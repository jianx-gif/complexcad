"""在 ComplexCAD 测试子集上跑 CAD-Recode 推理, 输出预测的 CadQuery 代码到
predictions/cadrecode/<uuid>.py。基于官方 demo.ipynb, 去掉可视化依赖:
  - 用 attn_implementation='sdpa'(torch 内置) 代替 flash_attention_2
  - 用 numpy FPS 代替 pytorch3d.sample_farthest_points
  - 直接用 output/<uuid>/point_cloud.npy(8192点)做输入, 不需 open3d/trimesh
输入预处理与 demo 一致: 归一化到边长2、中心在原点的立方体, 再 FPS 到 256 点。
可断点续跑(跳过已有预测)。用法: python run_cadrecode.py [--limit N]
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, sys, argparse, time
import numpy as np
import torch
from torch import nn
from transformers import AutoTokenizer, Qwen2ForCausalLM, Qwen2Model, PreTrainedModel
from transformers.modeling_outputs import CausalLMOutputWithPast

ROOT = _ROOT
OUTDIR = os.path.join(ROOT, "output")
SUBSET = os.path.join(ROOT, "predictions", "test_subset.txt")
PRED = os.path.join(ROOT, "predictions", "cadrecode")
MODEL_ID = "filapro/cad-recode-v1.5"


# ==== 模型定义(逐字取自官方 demo.ipynb) ====
class FourierPointEncoder(nn.Module):
    def __init__(self, hidden_size):
        super().__init__()
        frequencies = 2.0 ** torch.arange(8, dtype=torch.float32)
        self.register_buffer('frequencies', frequencies, persistent=False)
        self.projection = nn.Linear(51, hidden_size)

    def forward(self, points):
        x = points
        x = (x.unsqueeze(-1) * self.frequencies).view(*x.shape[:-1], -1)
        x = torch.cat((points, x.sin(), x.cos()), dim=-1)
        return self.projection(x)


class CADRecode(Qwen2ForCausalLM):
    def __init__(self, config):
        PreTrainedModel.__init__(self, config)
        self.model = Qwen2Model(config)
        self.vocab_size = config.vocab_size
        self.lm_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False)
        torch.set_default_dtype(torch.float32)
        self.point_encoder = FourierPointEncoder(config.hidden_size)
        torch.set_default_dtype(torch.bfloat16)

    def forward(self, input_ids=None, attention_mask=None, point_cloud=None,
                position_ids=None, past_key_values=None, inputs_embeds=None,
                labels=None, use_cache=None, output_attentions=None,
                output_hidden_states=None, return_dict=None, cache_position=None):
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict
        if past_key_values is None or past_key_values.get_seq_length() == 0:
            assert inputs_embeds is None
            inputs_embeds = self.model.embed_tokens(input_ids)
            point_embeds = self.point_encoder(point_cloud).bfloat16()
            inputs_embeds[attention_mask == -1] = point_embeds.reshape(-1, point_embeds.shape[2])
            attention_mask[attention_mask == -1] = 1
            input_ids = None
            position_ids = None
        outputs = self.model(
            input_ids=input_ids, attention_mask=attention_mask, position_ids=position_ids,
            past_key_values=past_key_values, inputs_embeds=inputs_embeds, use_cache=use_cache,
            output_attentions=output_attentions, output_hidden_states=output_hidden_states,
            return_dict=return_dict, cache_position=cache_position)
        logits = self.lm_head(outputs[0]).float()
        if not return_dict:
            return (logits,) + outputs[1:]
        return CausalLMOutputWithPast(loss=None, logits=logits,
                                      past_key_values=outputs.past_key_values,
                                      hidden_states=outputs.hidden_states,
                                      attentions=outputs.attentions)

    def prepare_inputs_for_generation(self, *args, **kwargs):
        model_inputs = super().prepare_inputs_for_generation(*args, **kwargs)
        model_inputs['point_cloud'] = kwargs['point_cloud']
        return model_inputs


def fps_numpy(pts, k, seed=0):
    """最远点采样 pts(N,3)->(k,3)。"""
    n = len(pts)
    if n <= k:
        idx = np.random.default_rng(seed).choice(n, k, replace=True)
        return pts[idx]
    sel = np.zeros(k, dtype=np.int64)
    d = np.full(n, np.inf)
    rng = np.random.default_rng(seed)
    sel[0] = rng.integers(n)
    for i in range(1, k):
        d = np.minimum(d, np.sum((pts - pts[sel[i - 1]]) ** 2, axis=1))
        sel[i] = int(np.argmax(d))
    return pts[sel]


def preprocess(uuid):
    """output/<uuid>/point_cloud.npy -> 归一化到边长2立方体 + FPS 256。"""
    p = np.load(os.path.join(OUTDIR, uuid, "point_cloud.npy"))[:, :3].astype(np.float32)
    center = (p.min(0) + p.max(0)) / 2.0
    scale = 2.0 / max((p.max(0) - p.min(0)).max(), 1e-9)
    p = (p - center) * scale
    return fps_numpy(p, 256).astype(np.float32)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    os.makedirs(PRED, exist_ok=True)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print("device:", device, torch.cuda.get_device_name(0) if device == 'cuda' else "", flush=True)

    tokenizer = AutoTokenizer.from_pretrained('Qwen/Qwen2-1.5B',
                                              pad_token='<|im_end|>', padding_side='left')
    model = CADRecode.from_pretrained(MODEL_ID, torch_dtype='auto',
                                      attn_implementation='sdpa').eval().to(device)
    print("模型已加载", flush=True)

    uuids = [l.strip() for l in open(SUBSET, encoding="utf-8") if l.strip()]
    if args.limit:
        uuids = uuids[:args.limit]
    todo = [u for u in uuids if not os.path.isfile(os.path.join(PRED, u + ".py"))]
    print("待推理 %d / %d (已有 %d)" % (len(todo), len(uuids), len(uuids) - len(todo)), flush=True)

    im_start = tokenizer('<|im_start|>')['input_ids'][0]
    t0 = time.time(); ok = fail = 0
    for i, u in enumerate(todo, 1):
        try:
            pc = preprocess(u)
            input_ids = [tokenizer.pad_token_id] * len(pc) + [im_start]
            attn = [-1] * len(pc) + [1]
            with torch.no_grad():
                batch = model.generate(
                    input_ids=torch.tensor(input_ids).unsqueeze(0).to(device),
                    attention_mask=torch.tensor(attn).unsqueeze(0).to(device),
                    point_cloud=torch.tensor(pc).unsqueeze(0).to(device),
                    max_new_tokens=768, pad_token_id=tokenizer.pad_token_id)
            s = tokenizer.batch_decode(batch)[0]
            b = s.find('<|im_start|>') + 12
            e = s.find('<|endoftext|>')
            code = s[b:e] if e > b else s[b:]
            open(os.path.join(PRED, u + ".py"), "w", encoding="utf-8").write(code)
            ok += 1
        except Exception as ex:
            fail += 1
            print("  FAIL %s: %s" % (u[:8], str(ex)[:80]), flush=True)
        if i % 20 == 0:
            el = time.time() - t0
            print("  %d/%d ok%d fail%d %.2fs/件 ETA%.1fmin"
                  % (i, len(todo), ok, fail, el / i, (len(todo) - i) * el / i / 60), flush=True)
    print("完成: ok %d fail %d 用时 %.1fmin -> %s"
          % (ok, fail, (time.time() - t0) / 60, PRED), flush=True)


if __name__ == "__main__":
    main()
