"""在 ComplexCAD 测试子集上跑 Zero-To-CAD-Qwen3-VL-2B(分布内模型)推理。
输入 = 每个 uuid 的 8 张渲染视图 image_0..7.png(256x256, 4前4后), 与该模型训练渲染同源,
故为分布内(in-distribution)对照——用来验证"数据分布对了模型就能学复杂操作"。
照官方 model card 推理代码; flash-attn 换 sdpa(Windows); bf16; 温控 + 可断点续跑。
用法: python run_zero2cad.py [--limit N] [--names-file f] [--chunk 20] [--maxtemp 82] [--maxnew 1024]
"""
import os, sys, argparse, time, subprocess
from PIL import Image
import torch
from transformers import Qwen3VLForConditionalGeneration, AutoProcessor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUTDIR = os.path.join(ROOT, "output")
SUBSET = os.path.join(ROOT, "predictions", "test_subset.txt")
PRED = os.path.join(ROOT, "predictions", "zero2cad")
MODEL_ID = "ADSKAILab/Zero-To-CAD-Qwen3-VL-2B"
SYS = ("You are a CAD code assistant. Given multiple rendered views of a 3D shape, "
       "generate clean, well-structured CadQuery Python code that accurately reproduces "
       "the geometry.")


def views_of(uuid):
    return [Image.open(os.path.join(OUTDIR, uuid, "image_%d.png" % i)).convert("RGB")
            for i in range(8)]


def gpu_temp():
    try:
        return int(subprocess.run(["nvidia-smi", "--query-gpu=temperature.gpu",
                                   "--format=csv,noheader"], capture_output=True,
                                  text=True, timeout=10).stdout.strip().split("\n")[0])
    except Exception:
        return -1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--names-file", default=SUBSET)
    ap.add_argument("--chunk", type=int, default=20)
    ap.add_argument("--maxtemp", type=int, default=82)
    ap.add_argument("--maxnew", type=int, default=1024)
    args = ap.parse_args()
    os.makedirs(PRED, exist_ok=True)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("device:", device, gpu_temp(), "C", flush=True)
    processor = AutoProcessor.from_pretrained(MODEL_ID)
    model = Qwen3VLForConditionalGeneration.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16, attn_implementation="sdpa").eval().to(device)
    print("模型已加载", flush=True)

    uuids = [l.strip() for l in open(args.names_file, encoding="utf-8") if l.strip()]
    if args.limit:
        uuids = uuids[:args.limit]
    todo = [u for u in uuids if not os.path.isfile(os.path.join(PRED, u + ".py"))]
    print("待推理 %d / %d" % (len(todo), len(uuids)), flush=True)

    t0 = time.time(); ok = fail = 0
    for i, u in enumerate(todo, 1):
        try:
            views = views_of(u)
            messages = [
                {"role": "system", "content": SYS},
                {"role": "user", "content": [
                    *[{"type": "image", "image": v} for v in views],
                    {"type": "text", "text": "Generate CadQuery code for this shape."}]}]
            text = processor.apply_chat_template(messages, tokenize=False,
                                                 add_generation_prompt=True)
            inputs = processor(text=text, images=views, return_tensors="pt").to(model.device)
            with torch.no_grad():
                out = model.generate(**inputs, max_new_tokens=args.maxnew, do_sample=False)
            code = processor.batch_decode(out[:, inputs.input_ids.shape[1]:],
                                          skip_special_tokens=True)[0]
            open(os.path.join(PRED, u + ".py"), "w", encoding="utf-8").write(code)
            ok += 1
        except Exception as e:
            fail += 1
            print("  FAIL %s: %s" % (u[:8], str(e)[:100]), flush=True)
        if i % args.chunk == 0:
            t = gpu_temp(); el = time.time() - t0
            print("  %d/%d ok%d fail%d %.1fs/件 GPU %dC ETA%.1fmin"
                  % (i, len(todo), ok, fail, el/i, t, (len(todo)-i)*el/i/60), flush=True)
            if t >= args.maxtemp:
                print("  ⚠ GPU %dC >= %dC, 冷却 60s ..." % (t, args.maxtemp), flush=True)
                torch.cuda.empty_cache(); time.sleep(60)
    print("完成: ok %d fail %d 用时 %.1fmin -> %s"
          % (ok, fail, (time.time()-t0)/60, PRED), flush=True)


if __name__ == "__main__":
    main()
