"""隔离评分**单个**预测: exec 生成的 CadQuery 代码 + 算指标 vs GT, 打印一行 JSON。
本脚本设计为放进**独立子进程 + 硬超时**运行(见 score_safe.py): 即便预测代码产生
畸形几何让 OpenCASCADE 卡死/爆内存, 也只影响这一个短命子进程, 到点被杀, 不拖垮系统。
用法(通常由 score_safe.py 调): python score_one.py <uuid> <pred_path>
"""
import sys, os, json, math, ast
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUTDIR = os.path.join(ROOT, "output")
sys.path.insert(0, ROOT)

MODELING = {"extrude", "cutBlind", "cutThruAll", "revolve", "loft", "sweep",
            "chamfer", "fillet", "hole", "cboreHole", "cskHole", "box", "cylinder",
            "sphere", "wedge", "shell", "twistExtrude", "union", "cut", "intersect",
            "circle", "rect", "polygon", "polyline", "spline", "ellipse"}
COMPLEX = {"loft", "revolve", "sweep"}
TAU = 0.02


def parse_ops(code):
    try:
        tree = ast.parse(code)
    except Exception:
        return None
    return [n.func.attr for n in ast.walk(tree)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
            and n.func.attr in MODELING]


def exec_shape(code):
    import cadquery as cq
    from types import SimpleNamespace
    g = {"cq": cq, "SimpleNamespace": SimpleNamespace, "math": math, "__name__": "__x__"}
    exec(code, g)
    res = g.get("result")
    if res is None:
        for v in g.values():
            if isinstance(v, cq.Workplane):
                res = v
    if res is None:
        return None
    return res.val() if hasattr(res, "val") else res


def sample_surface(shape, n, tol=0.5):
    v, tris = shape.tessellate(tol)
    if not tris:
        return None
    V = np.array([p.toTuple() if hasattr(p, "toTuple") else (p.x, p.y, p.z)
                  for p in v], dtype=float)
    T = np.asarray(tris, dtype=np.int64)
    tv = V[T]
    areas = 0.5 * np.linalg.norm(np.cross(tv[:, 1] - tv[:, 0], tv[:, 2] - tv[:, 0]), axis=1)
    s = areas.sum()
    if s <= 0:
        return None
    rng = np.random.default_rng(12345)
    idx = rng.choice(len(T), size=n, p=areas / s)
    u = rng.random((n, 1)); w = rng.random((n, 1))
    over = (u + w > 1).flatten(); u[over] = 1 - u[over]; w[over] = 1 - w[over]
    tri = tv[idx]
    return tri[:, 0] + u * (tri[:, 1] - tri[:, 0]) + w * (tri[:, 2] - tri[:, 0])


def geom_metrics(pred_pts, gt_pts):
    # 预测与 GT **各按自己的包围盒**独立归一化到单位尺度(中心在原点), 消除坐标系/
    # 尺度/平移差异(如 CAD-Recode 输出在 ±100 而 GT 在真实毫米), 只比较形状。
    from scipy.spatial import cKDTree

    def _norm(p):
        c = (p.min(0) + p.max(0)) / 2.0
        s = float((p.max(0) - p.min(0)).max()) + 1e-9
        return (p - c) / s
    P = _norm(pred_pts); G = _norm(gt_pts)
    dPG, _ = cKDTree(G).query(P)
    dGP, _ = cKDTree(P).query(G)
    prec = float((dPG < TAU).mean()); rec = float((dGP < TAU).mean())
    return {"chamfer": float(dPG.mean() + dGP.mean()),
            "fscore": 2 * prec * rec / (prec + rec + 1e-9)}


def op_recovery(pred_ops, gt_ops):
    from collections import Counter
    gp, gg = Counter(pred_ops), Counter(gt_ops)
    tg, tp = set(gg), set(gp)
    inter = sum((gp & gg).values())
    return {"op_type_recall": len(tg & tp) / max(len(tg), 1),
            "op_count_recall": inter / max(sum(gg.values()), 1),
            "op_exact": bool(gp == gg)}


def main():
    uuid, pred_path = sys.argv[1], sys.argv[2]
    rec = {"uuid": uuid}
    try:
        meta = json.load(open(os.path.join(OUTDIR, uuid, "metadata.json"), encoding="utf-8"))
        raw = meta.get("cadquery_ops_json", "[]")
        gt_ops_j = json.loads(raw) if isinstance(raw, str) else raw
        gt_ops = [o["op_name"] for o in gt_ops_j if o.get("op_name") in MODELING]
        rec["complex"] = any(o in COMPLEX for o in gt_ops)
        gt_pc = np.load(os.path.join(OUTDIR, uuid, "point_cloud.npy"))[:, :3].astype(float)
        code = open(pred_path, encoding="utf-8").read()
        pred_ops = parse_ops(code)
        if pred_ops is not None:
            rec.update(op_recovery(pred_ops, gt_ops))
        shape = exec_shape(code)
        if shape is None:
            print(json.dumps({**rec, "valid": False, "status": "no_result"})); return
        vol = shape.Volume() if hasattr(shape, "Volume") else 0.0
        nsol = len(shape.Solids()) if hasattr(shape, "Solids") else 0
        rec["valid"] = bool(nsol >= 1 and vol > 1e-9)
        if not rec["valid"]:
            print(json.dumps({**rec, "status": "invalid"})); return
        pred_pc = sample_surface(shape, len(gt_pc))
        if pred_pc is None:
            print(json.dumps({**rec, "status": "no_mesh"})); return
        rec.update(geom_metrics(pred_pc, gt_pc))
        print(json.dumps({**rec, "status": "ok"}))
    except Exception as e:
        print(json.dumps({**rec, "valid": False, "status": "err",
                          "err": (type(e).__name__ + ": " + str(e))[:80]}))


if __name__ == "__main__":
    main()
