"""Ch6 评测 harness: 给某方法对 output/ 子集的预测(预测的 CadQuery 代码,
predictions/<method>/<uuid>.py), 逐件算指标, 按 GT 复杂度分层汇总:

  - L1 有效性:   预测代码能否执行成有效实体(单连通、正体积)。
  - 几何相似:    Chamfer Distance、F-score@tau(预测表面采样点 vs GT point_cloud.npy),
                 两者按 GT 包围盒对角线归一, 尺度/平移不变(旋转不校正, 见文末说明)。
  - 操作恢复L3:  预测操作(AST解析) vs GT 操作(metadata.cadquery_ops_json):
                 类型召回 / 计数召回 / 是否完全一致。
  - L2 参数:     留待有对齐操作时补(见 TODO)。

复用 Ch5 的执行+GT读取思路(eval_precision.py)。子进程隔离, 单件失败不拖垮整批。

--self-test: 用 GT 自己的 cadquery.py 当"预测", 应得 validity≈1 / CD≈0 / F≈1 /
             op_type_recall≈1 —— 用来**验证 harness 本身正确**(不是方法对比结果)。

用法:
  # 验证 harness(拿 GT 当预测, 抽 30 件):
  python -X utf8 eval_predictions.py --self-test --limit 30 --jobs 8
  # 评一个真实方法(预测代码放在 predictions/cadrecode/<uuid>.py):
  python -X utf8 eval_predictions.py --method cadrecode --pred-dir <dir> --names-file subset.txt
"""
import sys, os, glob, json, argparse, time, math, ast
import numpy as np
import multiprocessing as mp

HERE = os.path.dirname(os.path.abspath(__file__))     # koor/
PARENT = os.path.dirname(HERE)                         # 1m_Convert/
ROOT = os.path.dirname(PARENT)                          # data/
OUTDIR = os.path.join(ROOT, "output")
REPORT = os.path.join(PARENT, "precision_report")

# 与 eval_precision.py 一致的"真实建模算子"白名单(过滤 faces/workplane 等链式辅助)
MODELING = {"extrude", "cutBlind", "cutThruAll", "revolve", "loft", "sweep",
            "chamfer", "fillet", "hole", "cboreHole", "cskHole", "box", "cylinder",
            "sphere", "wedge", "shell", "twistExtrude", "union", "cut", "intersect",
            "circle", "rect", "polygon", "polyline", "spline", "ellipse"}
COMPLEX = {"loft", "revolve", "sweep"}   # 定义"复杂操作"的核心集(章节焦点)
TAU = 0.02        # F-score 阈值(占归一化对角线的比例)
FSEED = 12345     # 采样可复现

_W = {}


def _winit():
    sys.path.insert(0, ROOT)
    import cadquery as cq
    from types import SimpleNamespace
    _W["cq"] = cq
    _W["ns"] = SimpleNamespace


def parse_ops(code):
    """AST 解析代码里的建模算子名(在 MODELING 白名单内)。返回列表或 None(语法错)。"""
    try:
        tree = ast.parse(code)
    except Exception:
        return None
    ops = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in MODELING:
                ops.append(node.func.attr)
    return ops


def exec_shape(code):
    cq = _W["cq"]
    g = {"cq": cq, "SimpleNamespace": _W["ns"], "math": math, "__name__": "__cqx__"}
    exec(code, g)
    res = g.get("result")
    if res is None:
        for v in g.values():
            if isinstance(v, cq.Workplane):
                res = v
    if res is None:
        return None
    return res.val() if hasattr(res, "val") else res


def sample_surface(shape, n, tol=0.3):
    """表面按三角面积加权采 n 个点。返回 (n,3) 或 None。"""
    v, tris = shape.tessellate(tol)
    if not tris:
        return None
    V = np.array([p.toTuple() if hasattr(p, "toTuple") else (p.x, p.y, p.z)
                  for p in v], dtype=float)
    T = np.asarray(tris, dtype=np.int64)
    tv = V[T]                                   # (m,3,3)
    a = tv[:, 1] - tv[:, 0]
    b = tv[:, 2] - tv[:, 0]
    areas = 0.5 * np.linalg.norm(np.cross(a, b), axis=1)
    s = areas.sum()
    if s <= 0:
        return None
    rng = np.random.default_rng(FSEED)
    idx = rng.choice(len(T), size=n, p=areas / s)
    u = rng.random((n, 1)); w = rng.random((n, 1))
    over = (u + w > 1).flatten()
    u[over] = 1 - u[over]; w[over] = 1 - w[over]
    tri = tv[idx]
    return tri[:, 0] + u * (tri[:, 1] - tri[:, 0]) + w * (tri[:, 2] - tri[:, 0])


def geom_metrics(pred_pts, gt_pts):
    # 预测与 GT **各按自己的包围盒**独立归一化到单位尺度(消除坐标系/尺度/平移差异,
    # 只比形状); 对不同坐标系输出(如 CAD-Recode 的 ±100 vs GT 毫米)才公平。
    from scipy.spatial import cKDTree

    def _norm(p):
        c = (p.min(0) + p.max(0)) / 2.0
        s = float((p.max(0) - p.min(0)).max()) + 1e-9
        return (p - c) / s
    P = _norm(pred_pts)
    G = _norm(gt_pts)
    dPG, _ = cKDTree(G).query(P)      # pred -> gt
    dGP, _ = cKDTree(P).query(G)      # gt -> pred
    prec = float((dPG < TAU).mean())
    rec = float((dGP < TAU).mean())
    return {"chamfer": float(dPG.mean() + dGP.mean()),
            "fscore": 2 * prec * rec / (prec + rec + 1e-9),
            "precision": prec, "recall": rec}


def op_recovery(pred_ops, gt_ops):
    from collections import Counter
    gp, gg = Counter(pred_ops), Counter(gt_ops)
    tg, tp = set(gg), set(gp)
    inter = sum((gp & gg).values())
    return {"op_type_recall": len(tg & tp) / max(len(tg), 1),
            "op_count_recall": inter / max(sum(gg.values()), 1),
            "op_exact": bool(gp == gg)}


def eval_one(task):
    uuid, pred_path, selftest = task
    d = os.path.join(OUTDIR, uuid)
    rec = {"uuid": uuid}
    try:
        meta = json.load(open(os.path.join(d, "metadata.json"), encoding="utf-8"))
        raw = meta.get("cadquery_ops_json", "[]")
        gt_ops_j = json.loads(raw) if isinstance(raw, str) else raw
        gt_ops = [o["op_name"] for o in gt_ops_j if o.get("op_name") in MODELING]
        rec["complex"] = any(o in COMPLEX for o in gt_ops)
        gt_pc = np.load(os.path.join(d, "point_cloud.npy"))[:, :3].astype(float)
        code = (open(os.path.join(d, "cadquery.py"), encoding="utf-8").read()
                if selftest else open(pred_path, encoding="utf-8").read())
        pred_ops = parse_ops(code)
        if pred_ops is not None:
            rec.update(op_recovery(pred_ops, gt_ops))
        shape = exec_shape(code)
        if shape is None:
            return {**rec, "valid": False, "status": "no_result"}
        vol = shape.Volume() if hasattr(shape, "Volume") else 0.0
        nsol = len(shape.Solids()) if hasattr(shape, "Solids") else 0
        rec["valid"] = bool(nsol >= 1 and vol > 1e-9)
        if not rec["valid"]:
            return {**rec, "status": "invalid_geom"}
        pred_pc = sample_surface(shape, len(gt_pc))
        if pred_pc is None:
            return {**rec, "status": "no_mesh"}
        rec.update(geom_metrics(pred_pc, gt_pc))
        return {**rec, "status": "ok"}
    except SyntaxError as e:
        return {**rec, "valid": False, "status": "syntax_error", "err": str(e)[:80]}
    except Exception as e:
        return {**rec, "valid": False, "status": "exec_error",
                "err": f"{type(e).__name__}: {e}"[:80]}


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return float(np.mean(xs)) if xs else float("nan")


def summarize(recs, method):
    def bucket(rs, label):
        ok = [r for r in rs if r.get("status") == "ok"]
        n = len(rs)
        print("  %-9s N=%-4d valid=%.1f%%  CD=%.4f  F=%.3f  "
              "opType=%.2f opCount=%.2f exact=%.1f%%"
              % (label, n,
                 100 * _mean([r.get("valid", False) for r in rs]),
                 _mean([r.get("chamfer") for r in ok]),
                 _mean([r.get("fscore") for r in ok]),
                 _mean([r.get("op_type_recall") for r in rs]),
                 _mean([r.get("op_count_recall") for r in rs]),
                 100 * _mean([r.get("op_exact") for r in rs])), flush=True)
    print("\n===== 方法 [%s] 汇总 (n=%d) =====" % (method, len(recs)), flush=True)
    bucket(recs, "ALL")
    bucket([r for r in recs if not r.get("complex")], "simple")
    bucket([r for r in recs if r.get("complex")], "complex")


def pick_uuids(limit, names_file):
    if names_file:
        want = [l.strip() for l in open(names_file, encoding="utf-8") if l.strip()]
        return [u for u in want if os.path.isfile(os.path.join(OUTDIR, u, "cadquery.py"))]
    us = []
    for d in sorted(glob.glob(os.path.join(OUTDIR, "*/"))):
        u = os.path.basename(os.path.normpath(d))
        if os.path.isfile(os.path.join(d, "cadquery.py")):
            us.append(u)
        if limit and len(us) >= limit:
            break
    return us


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", default="selftest")
    ap.add_argument("--pred-dir", default=None, help="predictions/<method>/, 内含 <uuid>.py")
    ap.add_argument("--self-test", action="store_true", help="用 GT 代码当预测, 验证 harness")
    ap.add_argument("--names-file", default=None, help="测试子集 uuid 清单(每行一个)")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--jobs", type=int, default=8)
    args = ap.parse_args()
    os.makedirs(REPORT, exist_ok=True)

    uuids = pick_uuids(args.limit, args.names_file)
    tasks = []
    for u in uuids:
        pp = None if args.self_test else os.path.join(args.pred_dir or "", u + ".py")
        if args.self_test or (pp and os.path.isfile(pp)):
            tasks.append((u, pp, args.self_test))
    print("待评 %d 件 (method=%s, self_test=%s, jobs=%d)"
          % (len(tasks), args.method, args.self_test, args.jobs), flush=True)
    if not tasks:
        print("无可评样本。", flush=True)
        return

    t0 = time.time()
    recs = []
    # 2026-09-08: 每件单独提交 + 结果超时 + 看门狗杀掉 RSS > 3 GB 的工作进程
    # (一个病态预测程序曾让 OCC 吞掉 56 GB 虚拟内存, 耗尽系统提交内存并拖垮了 GPU 训练).
    import threading, psutil
    stop = threading.Event()
    killed = {"n": 0}

    def watchdog(pool):
        while not stop.is_set():
            for w in list(pool._pool):
                try:
                    if psutil.Process(w.pid).memory_info().rss > 3 * 2**30:
                        psutil.Process(w.pid).kill(); killed["n"] += 1
                        print("  [watchdog] killed worker %d (>3 GB)" % w.pid, flush=True)
                except psutil.Error:
                    pass
            stop.wait(0.5)

    with mp.Pool(args.jobs, initializer=_winit) as pool:
        th = threading.Thread(target=watchdog, args=(pool,), daemon=True); th.start()
        pending = [(t, pool.apply_async(eval_one, (t,))) for t in tasks]
        for i, (t, ar) in enumerate(pending, 1):
            try:
                rec = ar.get(timeout=300)
            except mp.TimeoutError:
                rec = {"uuid": t[0], "status": "timeout_or_killed"}
            except Exception as e:
                rec = {"uuid": t[0], "status": "worker_error", "err": str(e)[:80]}
            recs.append(rec)
            if i % 50 == 0:
                print("  %d/%d  %.1f件/s" % (i, len(tasks), i / (time.time() - t0)),
                      flush=True)
        stop.set()
    if killed["n"]:
        print("  watchdog killed %d worker(s)" % killed["n"], flush=True)
    out = os.path.join(REPORT, "pred_metrics_%s.jsonl" % args.method)
    with open(out, "w", encoding="utf-8") as fh:
        for r in recs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    st = {}
    for r in recs:
        st[r.get("status", "?")] = st.get(r.get("status", "?"), 0) + 1
    print("状态分布: %s" % st, flush=True)
    summarize(recs, args.method)
    print("\n每件指标 -> %s  用时 %.1fmin" % (out, (time.time() - t0) / 60), flush=True)


if __name__ == "__main__":
    main()
