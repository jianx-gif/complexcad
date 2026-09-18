"""任务4: 数据集建模精度评估 (Modeling Precision Evaluation).

论文核心论点: 评估的是 **建模精度(参数/拓扑/复现精度)**, 而非仅几何相似度。
对 output/ 下每个件:
  1. 代码执行验证: 执行 cadquery.py -> 几何有效性(非空/实体/可度量)。异常分类。
  2. 复现精度: 重建几何的 bbox / 拓扑(faces,edges,vertices) vs metadata.geometry_stats GT
     -> 复现误差(代码能否精确复现原模型)。
  3. 操作覆盖: 从 cadquery_ops_json 统计 op_name 分布(Loft/Revolve/Sweep/Chamfer/Fillet...)。
  4. 复杂度: ops_count / face_count 分布。
  5. 精度-复杂度相关。

常驻 worker(import cadquery 一次) + multiprocessing Pool 并行 + 断点续传(已评估件跳过)。
输出 precision_report/metrics.jsonl (每件一行原始指标) 供后续 build_report 汇总出图。

用法: python -X utf8 eval_precision.py [--jobs N] [--limit N] [--resume]
"""
import sys, os, glob, json, argparse, time, math
import multiprocessing as mp

HERE = os.path.dirname(os.path.abspath(__file__))         # koor/
PARENT = os.path.dirname(HERE)                            # 1m_Convert/
ROOT = os.path.dirname(PARENT)                            # data/
OUTDIR = os.path.join(ROOT, "output")
REPORT = os.path.join(PARENT, "precision_report")
METRICS = os.path.join(REPORT, "metrics.jsonl")

_W = {}


def _winit():
    sys.path.insert(0, ROOT)
    import cadquery as cq
    from types import SimpleNamespace
    _W["cq"] = cq
    _W["ns"] = SimpleNamespace


def _geom_metrics(uuid):
    """执行 cadquery.py, 提取完整几何指标 + 与 GT 对比。返回 dict。"""
    cq = _W["cq"]
    d = os.path.join(OUTDIR, uuid)
    rec = {"uuid": uuid}
    # --- 读 GT ---
    try:
        meta = json.load(open(os.path.join(d, "metadata.json"), encoding="utf-8"))
    except Exception as e:
        return {"uuid": uuid, "status": "no_metadata", "err": str(e)[:60]}
    gs = meta.get("geometry_stats", {}) or {}
    ops_raw = meta.get("cadquery_ops_json", "[]")
    try:
        ops = json.loads(ops_raw) if isinstance(ops_raw, str) else ops_raw
    except Exception:
        ops = []
    rec["ops_count"] = meta.get("cadquery_ops_count", len(ops))
    # 操作类型(只统计真实建模算子, 过滤掉 faces/workplane/int/range 等链式辅助)
    MODELING = {"extrude", "cutBlind", "cutThruAll", "revolve", "loft", "sweep",
                "chamfer", "fillet", "hole", "cboreHole", "cskHole", "box", "cylinder",
                "sphere", "wedge", "shell", "twistExtrude", "union", "cut", "intersect",
                "circle", "rect", "polygon", "polyline", "spline", "ellipse"}
    op_names = [o.get("op_name") for o in ops if o.get("op_name") in MODELING]
    rec["ops"] = op_names
    rec["gt"] = {"num_faces": gs.get("num_faces"), "num_edges": gs.get("num_edges"),
                 "num_vertices": gs.get("num_vertices"), "bbox_dims": gs.get("bbox_dims")}
    # --- 执行源码, 重建几何 ---
    try:
        src = open(os.path.join(d, "cadquery.py"), encoding="utf-8").read()
    except Exception as e:
        return {**rec, "status": "no_source", "err": str(e)[:60]}
    t0 = time.time()
    try:
        g = {"cq": cq, "SimpleNamespace": _W["ns"], "math": math, "__name__": "__cqexec__"}
        exec(src, g)
        res = g.get("result")
        if res is None:
            for v in g.values():
                if isinstance(v, cq.Workplane):
                    res = v
        if res is None:
            return {**rec, "status": "no_result"}
        shape = res.val() if hasattr(res, "val") else res
        # 几何有效性 + 拓扑计数
        try:
            solids = shape.Solids() if hasattr(shape, "Solids") else []
            n_solids = len(solids)
        except Exception:
            n_solids = -1
        try:
            vol = shape.Volume() if hasattr(shape, "Volume") else 0.0
        except Exception:
            vol = -1.0
        try:
            nf = len(shape.Faces()); ne = len(shape.Edges()); nv = len(shape.Vertices())
        except Exception:
            nf = ne = nv = -1
        bb = shape.BoundingBox()
        rec["exec_ms"] = round((time.time() - t0) * 1000, 1)
        rec["rebuilt"] = {"num_faces": nf, "num_edges": ne, "num_vertices": nv,
                          "bbox_dims": [round(bb.xlen, 4), round(bb.ylen, 4), round(bb.zlen, 4)],
                          "volume": round(vol, 4), "n_solids": n_solids}
        # 有效性判定
        valid = (n_solids >= 1 and vol > 1e-9 and nf > 0)
        rec["valid"] = bool(valid)
        # 复现精度: 拓扑一致 + bbox 误差
        if gs.get("num_faces") is not None and nf >= 0:
            rec["topo_match"] = (nf == gs["num_faces"] and ne == gs.get("num_edges")
                                 and nv == gs.get("num_vertices"))
            rec["dface"] = nf - gs["num_faces"]
        if gs.get("bbox_dims") and bb is not None:
            gd = gs["bbox_dims"]; rd = [bb.xlen, bb.ylen, bb.zlen]
            # 复现 bbox 最大相对误差
            errs = [abs(a - b) / max(abs(b), 1e-6) for a, b in zip(rd, sorted(gd, reverse=False) if False else gd)]
            rec["bbox_rel_err"] = round(max(errs), 6)
            rec["bbox_abs_err"] = round(max(abs(a - b) for a, b in zip(rd, gd)), 6)
        rec["status"] = "ok" if valid else "invalid_geom"
        return rec
    except SyntaxError as e:
        return {**rec, "status": "syntax_error", "err": str(e)[:80]}
    except Exception as e:
        return {**rec, "status": "exec_error", "err": f"{type(e).__name__}: {e}"[:80]}


def _do(uuid):
    try:
        return _geom_metrics(uuid)
    except Exception as e:
        return {"uuid": uuid, "status": "worker_crash", "err": f"{type(e).__name__}: {e}"[:80]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--resume", action="store_true", help="跳过已在 metrics.jsonl 的件")
    args = ap.parse_args()
    os.makedirs(REPORT, exist_ok=True)

    done = set()
    if args.resume and os.path.isfile(METRICS):
        for line in open(METRICS, encoding="utf-8"):
            try:
                done.add(json.loads(line)["uuid"])
            except Exception:
                pass
        print(f"[resume] 已评估 {len(done)} 件, 跳过", flush=True)

    uuids = []
    for d in sorted(glob.glob(os.path.join(OUTDIR, "*/"))):
        u = os.path.basename(os.path.normpath(d))
        if not u or u in done:
            continue
        if os.path.isfile(os.path.join(d, "cadquery.py")):
            uuids.append(u)
        if args.limit and len(uuids) >= args.limit:
            break
    print(f"待评估 {len(uuids)} 件, jobs={args.jobs}", flush=True)
    if not uuids:
        print("无待办。", flush=True)
        return

    t0 = time.time()
    n = 0
    mode = "a" if (args.resume and os.path.isfile(METRICS)) else "w"
    with open(METRICS, mode, encoding="utf-8") as fh, \
            mp.Pool(args.jobs, initializer=_winit) as pool:
        for rec in pool.imap_unordered(_do, uuids, chunksize=4):
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
            if n % 100 == 0:
                fh.flush()
                el = time.time() - t0
                rate = n / el if el else 0
                eta = (len(uuids) - n) / rate if rate else 0
                print(f"  {n}/{len(uuids)}  {rate:.1f}件/s  ETA {eta/60:.1f}min", flush=True)
    print(f"\n评估完成: {n} 件, 用时 {(time.time()-t0)/60:.1f}min -> {METRICS}", flush=True)


if __name__ == "__main__":
    main()
