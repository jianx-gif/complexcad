# -*- coding: utf-8 -*-
"""实验P (闭环): cadrille 在 ComplexCAD 全量训练集上的 LoRA 微调 (同模型、训练前后对照).
与 pilot 的区别:
  * 训练集 6825 件 (泄漏防护后, 去注释程序 <= 1500 字符, 12 GB 显存余量), 验证集同标准;
  * 点云约定与推理一致: 网格坐标(mm)/100, 不居中 (cadrille 自身的训练约定, 代码单位 = 输入单位×100);
    pilot 的失败原因: 训练用 /100 不居中, 推理却用单位立方体居中 -> 输入分布错位;
  * 点云编码器 (FourierPointEncoder) 一并训练 (modules_to_save);
  * 2 epoch, LoRA r=16, lr 1e-4 cosine, batch 1 x accum 8, 梯度检查点, bf16, 断点续训, GPU 温控.
用法: python train_closed_loop.py [--data DIR] [--out DIR] [--epochs N] [--lr F]
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os
import sys, time, argparse, subprocess
from functools import partial

import torch
from transformers import AutoProcessor, Trainer, TrainingArguments, TrainerCallback
from peft import LoraConfig, get_peft_model

from cadrille import Cadrille, collate
from dataset import CadRecodeDataset
from train_closed_loop_utils import load_drawing

ap = argparse.ArgumentParser()
ap.add_argument('--data', default=_ROOT + '/_review/cc_full')
ap.add_argument('--out', default=_ROOT + '/_review/cc_full_lora')
ap.add_argument('--epochs', type=float, default=2)
ap.add_argument('--lr', type=float, default=1e-4)
ap.add_argument('--rank', type=int, default=16)
ap.add_argument('--maxtemp', type=int, default=80)
ap.add_argument('--step-sleep', type=float, default=0.5, help='每步后固定歇息秒数 (降低平均功耗/温度)')
ap.add_argument('--max-vram', type=float, default=11.0, help='GB; 超过则清缓存并暂停 (驱动挂死保护)')
ap.add_argument('--max-chars', type=int, default=0, help='>0: 训练/验证只用去注释程序 <= 该字符数的样本')
ap.add_argument('--joint', default='none', choices=['none', 'text', 'drawing'],
                help='联合输入: text = 点云 + description.txt; drawing = 点云 + drawing.png (工程图)')
ap.add_argument('--draw-tokens', type=int, default=600, help='工程图最多占用的视觉 token 数 (28x28 像素/token)')
ap.add_argument('--n-points', type=int, default=256)
ap.add_argument('--max-steps', type=int, default=-1, help='>0: 冒烟测试, 只跑这么多步')
ap.add_argument('--sampler', default='bucket', choices=['bucket', 'random'],
                help='训练样本顺序: bucket = 按程序长度分桶 (09-09 起的默认); random = HF 默认随机采样 (09-08 的 ComplexCAD/对照臂所用)')
ap.add_argument('--modal-dir', default=_ROOT + '/output', help='<uuid>/description.txt, drawing.png 所在目录')
args = ap.parse_args()
MODEL_ID = 'maksimko123/cadrille'
os.makedirs(args.out, exist_ok=True)
# 进程自己持有日志句柄 (昨夜的中断: 父进程重定向的 stderr 句柄失效 -> tqdm 写进度条抛 OSError 22)
_logf = open(os.path.join(args.out, 'stdout.txt'), 'a', buffering=1, encoding='utf-8')
sys.stdout = _logf; sys.stderr = _logf


_NVML = None


def gpu_temp():
    """进程内 NVML 读温度 (09-09: 四次无声消失/冻结的最后一行都是温控歇息, 之前每 2 步 spawn 一次 nvidia-smi 子进程; 改为不再 spawn)."""
    global _NVML
    try:
        if _NVML is None:
            import pynvml
            pynvml.nvmlInit(); _NVML = (pynvml, pynvml.nvmlDeviceGetHandleByIndex(0))
        pynvml, h = _NVML
        return int(pynvml.nvmlDeviceGetTemperature(h, pynvml.NVML_TEMPERATURE_GPU))
    except Exception:
        try:
            return int(subprocess.run(['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader'], capture_output=True,
                                      text=True, timeout=10, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)).stdout.strip().split('\n')[0])
        except Exception:
            return -1


class TempGuard(TrainerCallback):
    """温控 + 显存看门狗 (09-09 00:52 整机冻结: 显存 11.9/12.3 GB + 87C, 驱动挂死)."""
    def on_step_end(self, a, state, control, **kw):
        # 09-09 11:55: 90C 时 'CUDA error: unknown error' (RTX 4080 Laptop 目标温度 87C, 功耗上限不可设); 改为每 5 步检查, 超温即歇 30 s
        # 09-09 15:27 第五次整机冻结 (无日志/无转储, 显存无溢出, GPU 80C): 疑为持续满载下的散热/供电极限 -> 降占空比
        if args.step_sleep > 0:
            time.sleep(args.step_sleep)
        if state.global_step % 2 == 0:
            t = gpu_temp()
            if t >= args.maxtemp:
                print(f'[temp] GPU {t}C >= {args.maxtemp}C, cool 20s', flush=True)
                torch.cuda.empty_cache(); time.sleep(20)
        # 09-09 11:05: 变长样本让缓存分配器碎片化, reserved 在 10 步内从 4.7 冲到 16.5 GB (溢出到共享内存 -> 驱动挂死);
        # 每步清一次缓存 (毫秒级) 把 reserved 限制在单样本峰值附近; 超过阈值再额外暂停
        res = torch.cuda.memory_reserved() / 2**30
        torch.cuda.empty_cache()
        if res > args.max_vram:
            print(f'[vram] reserved {res:.2f} GB > {args.max_vram} GB after step {state.global_step}: pause 30 s', flush=True)
            time.sleep(30)
        if state.global_step % 20 == 0:
            print(f'[step {state.global_step}/{state.max_steps}] {time.strftime("%H:%M:%S")} gpu {gpu_temp()}C '
                  f'vram reserved {torch.cuda.memory_reserved() / 2**30:.2f} GB peak {torch.cuda.max_memory_reserved() / 2**30:.2f} GB', flush=True)


class JointDataset(torch.utils.data.Dataset):
    """在 CadRecodeDataset 的点云样本上附加第二模态 (与推理时 run_cadrille.py 的 pc_text / pc_draw 完全一致)."""

    def __init__(self, base, joint, modal_dir, draw_tokens):
        self.base, self.joint, self.modal_dir, self.draw_tokens = base, joint, modal_dir, draw_tokens

    def __len__(self):
        return len(self.base)

    def __getitem__(self, i):
        item = self.base[i]
        uuid = self.base.annotations[i]['uuid']
        if self.joint == 'text':
            desc = open(os.path.join(self.modal_dir, uuid, 'description.txt'), encoding='utf-8').read().strip()
            item['description'] = desc + chr(10) + 'Generate cadquery code'
        elif self.joint == 'drawing':
            item['image'] = load_drawing(os.path.join(self.modal_dir, uuid, 'drawing.png'), self.draw_tokens)
            item['description'] = 'The engineering drawing of the part is given. Generate cadquery code'
        return item


class BucketSampler(torch.utils.data.Sampler):
    """按程序长度分桶的随机采样: 相邻样本长度接近, 减少分配器碎片 (与 group_by_length 同理, 但长度 = 程序文件大小, 不用预加载网格)."""

    def __init__(self, lengths, bucket=32, seed=0):
        self.lengths, self.bucket, self.seed, self.epoch = list(lengths), bucket, seed, 0

    def __len__(self):
        return len(self.lengths)

    def __iter__(self):
        import random
        rng = random.Random(self.seed + self.epoch); self.epoch += 1
        idx = list(range(len(self.lengths))); rng.shuffle(idx)
        idx.sort(key=lambda i: self.lengths[i])
        buckets = [idx[i:i + self.bucket] for i in range(0, len(idx), self.bucket)]
        rng.shuffle(buckets)
        for b in buckets:
            rng.shuffle(b)
            for i in b:
                yield i


class SafeTrainer(Trainer):

    def _get_train_sampler(self, *a, **kw):
        if args.sampler == 'random':
            return super()._get_train_sampler(*a, **kw)
        ds = self.train_dataset
        base = ds.base if hasattr(ds, 'base') else ds
        return BucketSampler([os.path.getsize(x['py_path']) for x in base.annotations])

    """显存溢出 (分配器 OOM 或驱动级 CUDA OOM) 时跳过该样本而不是退出; 连续 3 次则放弃 (让外壳从检查点续跑)."""
    oom_streak = 0

    def training_step(self, model, inputs, num_items_in_batch=None):
        try:
            out = super().training_step(model, inputs, num_items_in_batch)
            self.oom_streak = 0
            return out
        except (torch.OutOfMemoryError, RuntimeError) as e:
            if 'out of memory' not in str(e).lower():
                raise
            self.oom_streak += 1
            print(f'[oom] step {self.state.global_step}: skipping batch ({self.oom_streak}/3)', flush=True)
            model.zero_grad(set_to_none=True)
            torch.cuda.empty_cache()
            if self.oom_streak >= 3:
                raise
            return torch.zeros((), device=self.args.device)


class LogFile(TrainerCallback):
    def on_log(self, a, state, control, logs=None, **kw):
        with open(os.path.join(args.out, 'log.txt'), 'a', encoding='utf-8') as f:
            f.write(f'{state.global_step} {logs}\n')


def main():
    os.makedirs(args.out, exist_ok=True)
    processor = AutoProcessor.from_pretrained('Qwen/Qwen2-VL-2B-Instruct',
                                              min_pixels=256 * 28 * 28, max_pixels=1280 * 28 * 28, padding_side='left')
    model = Cadrille.from_pretrained(MODEL_ID, torch_dtype=torch.bfloat16, attn_implementation='sdpa')
    model.config.use_cache = False
    model.enable_input_require_grads()
    lora = LoraConfig(r=args.rank, lora_alpha=2 * args.rank, lora_dropout=0.05, bias='none',
                      target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj', 'gate_proj', 'up_proj', 'down_proj'],
                      modules_to_save=['point_encoder'])
    model = get_peft_model(model, lora)
    model.print_trainable_parameters()

    ds_kw = dict(n_points=args.n_points, normalize_std_pc=100, noise_scale_pc=0.01, img_size=128,
                 normalize_std_img=200, noise_scale_img=-1, num_imgs=4, mode='pc')
    train_ds = CadRecodeDataset(root_dir=args.data, split='train', **ds_kw)
    val_ds = CadRecodeDataset(root_dir=args.data, split='val', **dict(ds_kw, noise_scale_pc=None))
    if args.max_chars > 0:
        for ds in (train_ds, val_ds):
            ds.annotations = [x for x in ds.annotations if os.path.getsize(x['py_path']) <= args.max_chars]
    if args.joint == 'drawing':
        # 4 of 9980 parts have no drawing (HLR timeout, Sec. 4): drop them (3 in the training set) instead of crashing mid-epoch
        for ds in (train_ds, val_ds):
            before = len(ds.annotations)
            ds.annotations = [x for x in ds.annotations if os.path.isfile(os.path.join(args.modal_dir, x['uuid'], 'drawing.png'))]
            if len(ds.annotations) != before:
                print(f'dropped {before - len(ds.annotations)} samples without drawing.png', flush=True)
    if args.joint != 'none':
        train_ds = JointDataset(train_ds, args.joint, args.modal_dir, args.draw_tokens)
        val_ds = JointDataset(val_ds, args.joint, args.modal_dir, args.draw_tokens)
    print('train', len(train_ds), 'val', len(val_ds), 'joint', args.joint, 'n_points', args.n_points, flush=True)

    resume = any(d.startswith('checkpoint-') for d in os.listdir(args.out))
    trainer = SafeTrainer(
        model=model,
        args=TrainingArguments(
            output_dir=args.out, per_device_train_batch_size=1, gradient_accumulation_steps=8,
            gradient_checkpointing=True, gradient_checkpointing_kwargs={'use_reentrant': False},
            dataloader_num_workers=0, num_train_epochs=args.epochs, max_steps=args.max_steps, lr_scheduler_type='cosine',
            learning_rate=args.lr, warmup_steps=50, weight_decay=0.01, bf16=True,
            remove_unused_columns=False, logging_steps=20, save_total_limit=2, disable_tqdm=True,
            save_strategy='steps', save_steps=100, eval_strategy='steps', eval_steps=800,
            per_device_eval_batch_size=1, report_to=[]),
        train_dataset=train_ds, eval_dataset=val_ds,
        data_collator=partial(collate, processor=processor, n_points=args.n_points),
        callbacks=[TempGuard(), LogFile()])
    trainer.train(resume_from_checkpoint=resume)
    model.save_pretrained(os.path.join(args.out, 'final_adapter'))
    print(f'peak vram reserved {torch.cuda.max_memory_reserved() / 2**30:.2f} GB', flush=True)
    print('TRAINING DONE ->', os.path.join(args.out, 'final_adapter'), flush=True)


if __name__ == '__main__':
    main()
