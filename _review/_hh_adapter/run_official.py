"""Sanity check of the released cadrille checkpoint (maksimko123/cadrille) on the OFFICIAL
evaluation data of its text and image branches.

Mirrors E:/3005/data/cadrille_repro/run_cadrille.py (the script used for our arms): same
processor settings, same Cadrille.from_pretrained(MODEL_ID, bf16, sdpa), same generate kwargs
(max_new_tokens=768, checkpoint generation_config = top_k 1 / temperature 0.01), same
batch_decode. Inputs come from the official loaders in cadrille_repro/dataset.py:
  text : Text2CADDataset(root_dir=data, split='test')       -> description only (no suffix)
  img  : CadRecodeDataset(split='deepcad_test_mesh', mode='img', img_size=128, num_imgs=4)
         -> 4 open3d renders, 2x2 grid, 'Generate cadquery code'
Predictions are written as <uid>+0.py so cadrille's evaluate.py convention can be used.
"""
import os, sys, argparse, time, json
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
REPRO = 'E:/3005/data/cadrille_repro'
sys.path.insert(0, HERE)
sys.path.insert(0, REPRO)
import o3d_stub  # noqa: F401  (isolated open3d for the official renderer)
import open3d
import dataset as ds_mod
ds_mod.open3d = open3d   # dataset.mesh_to_image references a module-level open3d name
from transformers import AutoProcessor
from cadrille import Cadrille, collate

MODEL_ID = 'maksimko123/cadrille'
MAX_NEW_TOKENS = 768
N_POINTS = 256
DATA = os.path.join(HERE, 'data')


def gen_kwargs(batch, device):
    kw = dict(input_ids=batch['input_ids'].to(device), attention_mask=batch['attention_mask'].to(device),
              point_clouds=batch['point_clouds'].to(device), is_pc=batch['is_pc'].to(device),
              is_img=batch['is_img'].to(device), max_new_tokens=MAX_NEW_TOKENS)
    for k in ('pixel_values_videos', 'video_grid_thw', 'pixel_values', 'image_grid_thw'):
        if batch.get(k) is not None:
            kw[k] = batch[k].to(device)
    return kw


_NVML = None


def gpu_temp():
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
    ap.add_argument('--mode', required=True, choices=['text', 'img', 'pc'])
    ap.add_argument('--subset', required=True)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--batch', type=int, default=4)
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--maxtemp', type=int, default=82)
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    want = [l.strip() for l in open(args.subset, encoding='utf-8') if l.strip()]
    if args.limit:
        want = want[:args.limit]

    if args.mode == 'text':
        ds = ds_mod.Text2CADDataset(root_dir=DATA, split='test')
        by_uid = {a['uid']: a for a in ds.annotations}
        ds.annotations = [by_uid[u] for u in want]
    else:
        ds = ds_mod.CadRecodeDataset(
            root_dir=DATA, split='deepcad_test_mesh', n_points=256, normalize_std_pc=100,
            noise_scale_pc=None, img_size=128, normalize_std_img=200, noise_scale_img=-1,
            num_imgs=4, mode=args.mode)   # 'img' or 'pc' (pc: official test normalisation (pc-0.5)*2)
        by_uid = {os.path.basename(a['mesh_path'])[:-4]: a for a in ds.annotations}
        ds.annotations = [by_uid[u] for u in want]
    names = want
    todo_idx = [i for i, u in enumerate(names)
                if not os.path.isfile(os.path.join(args.outdir, u + '+0.py'))]
    print('mode', args.mode, 'subset', len(names), 'todo', len(todo_idx), flush=True)

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print('device:', device, gpu_temp(), 'C', flush=True)
    processor = AutoProcessor.from_pretrained(
        'Qwen/Qwen2-VL-2B-Instruct', min_pixels=256 * 28 * 28, max_pixels=1280 * 28 * 28,
        padding_side='left')
    model = Cadrille.from_pretrained(MODEL_ID, torch_dtype=torch.bfloat16,
                                     attn_implementation='sdpa')
    model = model.eval().to(device)
    print('model loaded; generation_config:', model.generation_config.to_dict().get('do_sample'),
          model.generation_config.to_dict().get('top_k'), model.generation_config.to_dict().get('temperature'),
          flush=True)

    t0 = time.time(); ok = fail = 0; B = args.batch; timing = []
    for bi in range(0, len(todo_idx), B):
        grp = todo_idx[bi:bi + B]
        tb = time.time()
        try:
            items = [ds[i] for i in grp]
            batch = collate(items, processor, n_points=N_POINTS, eval=True)
            with torch.no_grad():
                gen = model.generate(**gen_kwargs(batch, device))
            trimmed = [o[len(inp):] for inp, o in zip(batch['input_ids'], gen)]
            codes = processor.batch_decode(trimmed, skip_special_tokens=True,
                                           clean_up_tokenization_spaces=False)
            for i, code in zip(grp, codes):
                with open(os.path.join(args.outdir, names[i] + '+0.py'), 'w', encoding='utf-8') as f:
                    f.write(code)
                ok += 1
        except Exception as e:
            fail += len(grp)
            print('  FAIL batch %s: %s' % (names[grp[0]], str(e)[:120]), flush=True)
        timing.append((len(grp), time.time() - tb))
        done_n = bi + len(grp)
        el = time.time() - t0
        t = gpu_temp()
        print('  %d/%d ok%d fail%d %.1fs/item GPU %dC ETA %.1fmin' % (
            done_n, len(todo_idx), ok, fail, el / max(1, done_n), t,
            (len(todo_idx) - done_n) * el / max(1, done_n) / 60), flush=True)
        if t >= args.maxtemp:
            print('  GPU %dC >= %dC, cooling 60s' % (t, args.maxtemp), flush=True)
            torch.cuda.empty_cache(); time.sleep(60)
    total = time.time() - t0
    print('done: ok %d fail %d %.1f min -> %s' % (ok, fail, total / 60, args.outdir), flush=True)
    with open(os.path.join(args.outdir, '_runtime.json'), 'w') as f:
        json.dump({'mode': args.mode, 'n': len(names), 'todo_this_run': len(todo_idx), 'ok': ok,
                   'fail': fail, 'seconds': total, 'batch': B, 'max_new_tokens': MAX_NEW_TOKENS,
                   'peak_vram_gb': torch.cuda.max_memory_allocated() / 2**30 if device == 'cuda' else None},
                  f, indent=1)


if __name__ == '__main__':
    main()
