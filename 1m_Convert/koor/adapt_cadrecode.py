"""把 ComplexCAD 点云适配成 CAD-Recode 推理输入(Ch6 加分实验用)。

只依赖 numpy。读 output/<uuid>/point_cloud.npy (8192x6 = XYZ+法向), 取 XYZ,
下采样到 CAD-Recode 期望的点数, 按其约定归一化, 写出到 adapted/<uuid>.npy。

>>> 有两个 [VERIFY] 参数, 必须对照 CAD-Recode 官方 README/代码填对, 否则精度虚低 <<<
  1) N_POINTS: CAD-Recode 期望的输入点数(论文/代码里定, 常见 256)。
  2) NORMALIZE: 归一化方式, 必须和仓库 demo 的预处理**完全一致**
     (常见: 去质心 + 缩放到单位球 [半径1] 或单位盒)。

用法:
  python -X utf8 adapt_cadrecode.py --names-file ../../predictions/test_subset.txt \
         --out ../../predictions/_cadrecode_input
"""
import os, sys, argparse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUTDIR = os.path.join(ROOT, "output")

# ==================== [VERIFY] 按 CAD-Recode 仓库改这两项 ====================
N_POINTS = 256          # 已确认: CAD-Recode 与 cadrille 均用 256 点(FPS 采样), 见
                        # cadrille 论文(arXiv 2505.22914) Table 1 脚注; 保险起见核对仓库
NORMALIZE = "official"   # 2026-09-17 核对 CAD-Recode 官方 demo.ipynb (github.com/filaPro/cad-recode):
                         #   mesh.apply_translation(-(bounds[0]+bounds[1])/2); mesh.apply_scale(2/max(extents))
                         #   即: 包围盒中心居中, 最大边长缩放到 2 (立方体 [-1,1]); 再 8192 面采样 -> FPS 256.
                         # 之前的 "unit_ball" (质心 + 半径 1) 与官方不一致 (predictions/cadrecode_unitball 保留作对比)。
# ===========================================================================


def farthest_point_sample(pts, n):
    """FPS 下采样到 n 点(比随机更均匀, 多数点云网络这么预处理)。"""
    m = len(pts)
    if m <= n:
        idx = np.random.default_rng(0).choice(m, n, replace=True)
        return pts[idx]
    sel = np.zeros(n, dtype=np.int64)
    d = np.full(m, np.inf)
    sel[0] = 0
    for i in range(1, n):
        d = np.minimum(d, np.sum((pts - pts[sel[i - 1]]) ** 2, axis=1))
        sel[i] = int(np.argmax(d))
    return pts[sel]


def normalize(pts):
    if NORMALIZE == "official":          # CAD-Recode demo.ipynb convention (verified 2026-09-17)
        c = (pts.min(0) + pts.max(0)) / 2.0
        s = 2.0 / max(float((pts.max(0) - pts.min(0)).max()), 1e-9)
        return (pts - c) * s
    c = pts.mean(0)
    p = pts - c
    if NORMALIZE == "unit_ball":
        s = np.max(np.linalg.norm(p, axis=1)) + 1e-9
        return p / s
    if NORMALIZE == "unit_box":
        s = np.max(np.abs(p)) + 1e-9
        return p / s
    return p            # [VERIFY] 若仓库用别的约定, 在此实现


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--names-file", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    names = [l.strip() for l in open(args.names_file, encoding="utf-8") if l.strip()]
    n_ok = 0
    for u in names:
        f = os.path.join(OUTDIR, u, "point_cloud.npy")
        if not os.path.isfile(f):
            continue
        xyz = np.load(f)[:, :3].astype(np.float32)
        xyz = farthest_point_sample(xyz, N_POINTS)
        xyz = normalize(xyz)
        np.save(os.path.join(args.out, u + ".npy"), xyz.astype(np.float32))
        n_ok += 1
    print("适配 %d 件 (N_POINTS=%d, NORMALIZE=%s) -> %s"
          % (n_ok, N_POINTS, NORMALIZE, args.out))
    print(">>> 若 CAD-Recode 精度异常低, 先核对 N_POINTS 与 NORMALIZE 两个 [VERIFY] <<<")


if __name__ == "__main__":
    main()
