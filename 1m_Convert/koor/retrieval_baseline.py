"""非学习检索基线(Ch6): 对每个测试件, 用点云在**训练池**(全库减去测试子集)里检索
最相似的件, 用它的 cadquery.py 当"预测"。这是一个诚实的、可本地跑的基线, 用来:
  (1) 端到端验证评测管线在**真实方法**(非 identity/random)上的行为;
  (2) 印证论文论点: 检索能拿到几何相近的形状(CD 尚可), 却几乎拿不对建模操作
      (op 恢复低)—— 即"几何相似 != 建模精度"。

描述子: 点云去质心 + 按包围盒对角线归一 -> G^3 体素占据(旋转敏感, 但件都已规范位姿)。
最近邻: 测试件 vs 训练池, L2 最近。输出 predictions/retrieval/<uuid>.py。

用法: python -X utf8 retrieval_baseline.py [--grid 10] [--jobs 8]
"""
import sys, os, glob, json, argparse, time
import numpy as np
import multiprocessing as mp

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
ROOT = os.path.dirname(PARENT)
OUTDIR = os.path.join(ROOT, "output")
PREDDIR = os.path.join(ROOT, "predictions", "retrieval")
SUBSET = os.path.join(ROOT, "predictions", "test_subset.txt")

G = 10


def _desc(uuid):
    """点云 -> 归一化体素占据描述子(G^3,)。失败返回 None。"""
    try:
        p = np.load(os.path.join(OUTDIR, uuid, "point_cloud.npy"))[:, :3].astype(np.float32)
    except Exception:
        return uuid, None
    c = p.mean(0)
    diag = float(np.linalg.norm(p.max(0) - p.min(0))) + 1e-9
    q = (p - c) / diag + 0.5                      # 大致落到 [0,1]
    idx = np.clip((q * G).astype(np.int32), 0, G - 1)
    vox = np.zeros((G, G, G), dtype=np.float32)
    vox[idx[:, 0], idx[:, 1], idx[:, 2]] = 1.0
    v = vox.ravel()
    n = np.linalg.norm(v) + 1e-9
    return uuid, (v / n)                           # 单位化 -> L2 最近 == 余弦最近


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=8)
    args = ap.parse_args()
    os.makedirs(PREDDIR, exist_ok=True)

    test = [l.strip() for l in open(SUBSET, encoding="utf-8") if l.strip()]
    test_set = set(test)
    all_uuids = [os.path.basename(os.path.normpath(d))
                 for d in sorted(glob.glob(os.path.join(OUTDIR, "*/")))
                 if os.path.isfile(os.path.join(d, "point_cloud.npy"))]
    print("全库 %d, 测试 %d, 训练池 %d" % (len(all_uuids), len(test),
                                          len(all_uuids) - len(test)), flush=True)

    t0 = time.time()
    desc = {}
    with mp.Pool(args.jobs) as pool:
        for i, (u, d) in enumerate(pool.imap_unordered(_desc, all_uuids, chunksize=16), 1):
            if d is not None:
                desc[u] = d
            if i % 2000 == 0:
                print("  描述子 %d/%d" % (i, len(all_uuids)), flush=True)
    print("描述子完成 %d 件, 用时 %.1fmin" % (len(desc), (time.time() - t0) / 60), flush=True)

    pool_ids = [u for u in all_uuids if u not in test_set and u in desc]
    M = np.stack([desc[u] for u in pool_ids])      # (P, G^3)
    n_ok = 0
    for u in test:
        if u not in desc:
            continue
        sims = M @ desc[u]                          # 余弦相似(已单位化)
        j = int(np.argmax(sims))
        nn = pool_ids[j]
        try:
            src = open(os.path.join(OUTDIR, nn, "cadquery.py"), encoding="utf-8").read()
            open(os.path.join(PREDDIR, u + ".py"), "w", encoding="utf-8").write(src)
            n_ok += 1
        except Exception:
            pass
    print("检索预测写出 %d 件 -> %s" % (n_ok, PREDDIR), flush=True)


if __name__ == "__main__":
    main()
