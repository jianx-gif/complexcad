"""在 ComplexCAD 测试子集上跑 cadrille(pc 模式)推理, 输出预测代码到
predictions/cadrille/<uuid>.py。基于官方 test.py + cadrille.collate, 去掉数据集脚手架,
直接用 output/<uuid>/point_cloud.npy 做输入。flash_attention_2 -> sdpa(Windows)。
小批次 + 每批查 GPU 温度(驱动不稳, 超温暂停冷却)。可断点续跑。
用法: python run_cadrille.py [--limit N] [--names-file f] [--chunk 25] [--maxtemp 82]
"""
import os, sys, argparse, time, subprocess
import numpy as np
from PIL import Image, ImageOps
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from transformers import AutoProcessor
from cadrille import Cadrille, collate

OUTDIR = os.path.join(ROOT, "output")
SUBSET = os.path.join(ROOT, "predictions", "test_subset.txt")
PRED = os.path.join(ROOT, "predictions", "cadrille")
MODEL_ID = "maksimko123/cadrille"


def fps(pts, k, seed=0):
    n = len(pts)
    if n <= k:
        return pts[np.random.default_rng(seed).choice(n, k, replace=True)]
    sel = np.zeros(k, np.int64); d = np.full(n, np.inf)
    sel[0] = 0
    for i in range(1, k):
        d = np.minimum(d, np.sum((pts - pts[sel[i-1]])**2, axis=1)); sel[i] = int(np.argmax(d))
    return pts[sel]


PC_SCALE100 = False       # 闭环微调模型: 训练约定 = 网格 mm 坐标 / 100, 不居中 (与 CadRecodeDataset train 一致)
MAX_NEW_TOKENS = 768
N_POINTS = 256
PC_DIR = None             # 若给定: 点云取 PC_DIR/<name>.npy (装配闭环: 融合装配体点云), 否则 output/<uuid>/point_cloud.npy
DRAW_TOKENS = 600


def preprocess(uuid):
    src = os.path.join(PC_DIR, uuid + ".npy") if PC_DIR else os.path.join(OUTDIR, uuid, "point_cloud.npy")
    p = np.load(src)[:, :3].astype(np.float32)
    p = fps(p, N_POINTS)
    if PC_SCALE100:
        return (p / 100.0).astype(np.float32)   # 与微调训练完全相同的输入约定
    c = (p.min(0) + p.max(0)) / 2.0
    s = 2.0 / max((p.max(0) - p.min(0)).max(), 1e-9)
    return ((p - c) * s).astype(np.float32)     # -> [-1,1] 立方体(与 cadrille test 一致)


def preprocess_img(uuid, size=128):
    """取 4 张视图 -> 各resize+黑边 -> 2x2 拼成单张(仿 cadrille num_imgs=4)。"""
    imgs = []
    for k in (0, 1, 2, 3):
        p = os.path.join(OUTDIR, uuid, "image_%d.png" % k)
        im = Image.open(p).convert("RGB").resize((size, size))
        imgs.append(ImageOps.expand(im, border=3, fill="black"))
    top = np.hstack((np.array(imgs[0]), np.array(imgs[1])))
    bot = np.hstack((np.array(imgs[2]), np.array(imgs[3])))
    return Image.fromarray(np.vstack((top, bot)))


def make_item(u, mode):
    """与训练 (train_closed_loop.JointDataset) 一致的输入构造."""
    if mode == "pc":
        return {"point_cloud": preprocess(u), "description": "Generate cadquery code", "file_name": u}
    if mode == "img":
        return {"video": [preprocess_img(u)], "description": "Generate cadquery code", "file_name": u}
    desc = None
    if mode in ("pc_text", "img_text", "text"):
        desc = open(os.path.join(OUTDIR, u, "description.txt"), encoding="utf-8").read().strip()
    if mode == "pc_text":
        return {"point_cloud": preprocess(u), "description": desc + chr(10) + "Generate cadquery code", "file_name": u}
    if mode == "img_text":
        return {"video": [preprocess_img(u)], "description": desc + chr(10) + "Generate cadquery code", "file_name": u}
    if mode == "pc_draw":
        from train_closed_loop_utils import load_drawing
        return {"point_cloud": preprocess(u), "image": load_drawing(os.path.join(OUTDIR, u, "drawing.png"), DRAW_TOKENS),
                "description": "The engineering drawing of the part is given. Generate cadquery code", "file_name": u}
    return {"description": desc, "file_name": u}


def gen_kwargs(batch, device):
    kw = dict(input_ids=batch["input_ids"].to(device), attention_mask=batch["attention_mask"].to(device),
              point_clouds=batch["point_clouds"].to(device), is_pc=batch["is_pc"].to(device),
              is_img=batch["is_img"].to(device), max_new_tokens=MAX_NEW_TOKENS)
    for k in ("pixel_values_videos", "video_grid_thw", "pixel_values", "image_grid_thw"):
        if batch.get(k) is not None:
            kw[k] = batch[k].to(device)
    return kw


_NVML = None


def gpu_temp():
    """进程内 NVML 读温度, 不再 spawn nvidia-smi 子进程 (见 train_closed_loop.gpu_temp)."""
    global _NVML
    try:
        if _NVML is None:
            import pynvml
            pynvml.nvmlInit(); _NVML = (pynvml, pynvml.nvmlDeviceGetHandleByIndex(0))
        pynvml, h = _NVML
        return int(pynvml.nvmlDeviceGetTemperature(h, pynvml.NVML_TEMPERATURE_GPU))
    except Exception:
        return -1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--names-file", default=SUBSET)
    ap.add_argument("--chunk", type=int, default=25)
    ap.add_argument("--mode", default="pc", choices=["pc", "text", "img", "pc_text", "img_text", "pc_draw"])
    ap.add_argument("--n-points", type=int, default=256)
    ap.add_argument("--pc-dir", default=None, help="点云目录 <name>.npy (装配闭环)")
    ap.add_argument("--draw-tokens", type=int, default=600)
    ap.add_argument("--maxtemp", type=int, default=82)
    ap.add_argument("--adapter", default=None, help="peft LoRA adapter 目录(微调评估)")
    ap.add_argument("--batch", type=int, default=1, help="批量推理大小(仅pc模式)")
    ap.add_argument("--outdir", default=None, help="覆盖预测输出目录名")
    ap.add_argument("--pc-scale100", action="store_true", help="点云用 mm/100 不居中 (闭环微调模型的训练约定)")
    ap.add_argument("--max-new-tokens", type=int, default=768)
    args = ap.parse_args()
    global PC_SCALE100, MAX_NEW_TOKENS, N_POINTS, PC_DIR, DRAW_TOKENS
    PC_SCALE100 = args.pc_scale100
    MAX_NEW_TOKENS = args.max_new_tokens
    N_POINTS = args.n_points; PC_DIR = args.pc_dir; DRAW_TOKENS = args.draw_tokens
    pred_dir = os.path.join(ROOT, "predictions", args.outdir or {
        "pc": "cadrille", "text": "cadrille_text", "img": "cadrille_img",
        "pc_text": "cadrille_pc_text", "img_text": "cadrille_img_text", "pc_draw": "cadrille_pc_draw"}[args.mode])
    os.makedirs(pred_dir, exist_ok=True)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("device:", device, gpu_temp(), "C", flush=True)
    processor = AutoProcessor.from_pretrained(
        "Qwen/Qwen2-VL-2B-Instruct", min_pixels=256*28*28, max_pixels=1280*28*28,
        padding_side="left")
    model = Cadrille.from_pretrained(MODEL_ID, torch_dtype=torch.bfloat16,
                                     attn_implementation="sdpa")
    if args.adapter:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, args.adapter).merge_and_unload()
        print("LoRA adapter merged:", args.adapter, flush=True)
    model = model.eval().to(device)
    print("模型已加载", flush=True)

    uuids = [l.strip() for l in open(args.names_file, encoding="utf-8") if l.strip()]
    if args.limit:
        uuids = uuids[:args.limit]
    todo = [u for u in uuids if not os.path.isfile(os.path.join(pred_dir, u + ".py"))]
    print("待推理 %d / %d (mode=%s)" % (len(todo), len(uuids), args.mode), flush=True)

    t0 = time.time(); ok = fail = 0
    if args.mode in ("pc", "pc_text", "pc_draw") and args.batch > 1:
        # 批量路径: 贪心+同一上限, 协议与单件一致
        B = args.batch
        for bi in range(0, len(todo), B):
            grp = todo[bi:bi + B]
            try:
                items = [make_item(u, args.mode) for u in grp]
                batch = collate(items, processor, n_points=N_POINTS, eval=True)
                with torch.no_grad():
                    gen = model.generate(**gen_kwargs(batch, device))
                trimmed = [o[len(inp):] for inp, o in zip(batch["input_ids"], gen)]
                codes = processor.batch_decode(trimmed, skip_special_tokens=True,
                                               clean_up_tokenization_spaces=False)
                for u, code in zip(grp, codes):
                    open(os.path.join(pred_dir, u + ".py"), "w",
                         encoding="utf-8").write(code)
                    ok += 1
            except Exception as e:
                fail += len(grp)
                print("  FAIL batch %s: %s" % (grp[0][:8], str(e)[:90]), flush=True)
            done_n = bi + len(grp)
            if done_n % (B * 4) < B:
                t = gpu_temp(); el = time.time() - t0
                print("  %d/%d ok%d fail%d %.1fs/件 GPU %dC ETA%.1fmin"
                      % (done_n, len(todo), ok, fail, el / max(1, done_n), t,
                         (len(todo) - done_n) * el / max(1, done_n) / 60), flush=True)
                if t >= args.maxtemp:
                    print("  ⚠ GPU %dC, 冷却 60s ..." % t, flush=True)
                    torch.cuda.empty_cache(); time.sleep(60)
        print("完成: ok %d fail %d 用时 %.1fmin -> %s"
              % (ok, fail, (time.time() - t0) / 60, pred_dir), flush=True)
        return

    for i, u in enumerate(todo, 1):
        try:
            item = make_item(u, args.mode)
            batch = collate([item], processor, n_points=N_POINTS, eval=True)
            with torch.no_grad():
                gen = model.generate(**gen_kwargs(batch, device))
            trimmed = [o[len(inp):] for inp, o in zip(batch["input_ids"], gen)]
            code = processor.batch_decode(trimmed, skip_special_tokens=True,
                                          clean_up_tokenization_spaces=False)[0]
            open(os.path.join(pred_dir, u + ".py"), "w", encoding="utf-8").write(code)
            ok += 1
        except Exception as e:
            fail += 1
            print("  FAIL %s: %s" % (u[:8], str(e)[:90]), flush=True)
        if i % args.chunk == 0:
            t = gpu_temp(); el = time.time() - t0
            print("  %d/%d ok%d fail%d %.1fs/件 GPU %dC ETA%.1fmin"
                  % (i, len(todo), ok, fail, el/i, t, (len(todo)-i)*el/i/60), flush=True)
            if t >= args.maxtemp:
                print("  ⚠ GPU %dC >= %dC, 冷却 60s ..." % (t, args.maxtemp), flush=True)
                torch.cuda.empty_cache(); time.sleep(60)
    print("完成: ok %d fail %d 用时 %.1fmin -> %s"
          % (ok, fail, (time.time()-t0)/60, pred_dir), flush=True)


if __name__ == "__main__":
    main()
