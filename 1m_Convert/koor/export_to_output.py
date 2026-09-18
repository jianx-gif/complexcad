"""Materialize converted test-split models into a SELF-CONTAINED test directory
1m_Convert/output_koor/<uuid>/ -- this is the koor (quantization) test build and
must NOT touch the finished drawings under the top-level output/.

Per the chosen options:
  - cadquery.py        <- cadquery_file_orig (true-mm code)
  - model.step/.stl    <- step_file / stl_file binaries from the ORIGINAL parquet
  - image_0..7.png     <- image_N binaries from the ORIGINAL parquet
  - metadata.json      <- 7 scalar stat columns (ops_json normalised to op_name list)
  - koor.json          <- scale, offs, max_dim_mm, converted code (quantization gt)
  - drawing.{png,svg,dxf}        <- make_drawings.process (OUT redirected here)
  - point_cloud / brep / desc    <- augment_data.augment (OUT redirected here)

Usage: python export_to_output.py [N]   (default 20; 0 = all kept models)
"""
import sys, os, glob, json, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)          # 1m_Convert/ (脚本移入 koor/ 后, 数据目录在上一级)
ROOT = os.path.dirname(PARENT)          # project root
if importlib.util.find_spec("make_drawings") is None:   # not pip-installed (complexcad-koor): run from the checkout
    sys.path.insert(0, ROOT)            # import the pipeline modules from project root

OUT = os.path.join(PARENT, "output_koor")   # <-- isolated test output
CONV = os.path.join(PARENT, "_testrun", "out", "test.parquet")
REC = os.path.join(PARENT, "_testrun", "rec", "test.rec.parquet")
ORIG_GLOB = os.path.join(ROOT, "test", "*.parquet")

SCALAR_COLS = ["uuid", "num_faces", "face_latency_ms", "cadquery_ops_json",
               "cadquery_ops_count", "ops_latency_ms", "num_renders"]
IMG_COLS = [f"image_{i}" for i in range(8)]


def _b(v):
    return bytes(v) if isinstance(v, (bytes, bytearray)) else v


def load_converted(n):
    import pyarrow.parquet as pq
    want = {}
    for path in (CONV, REC):
        if not os.path.exists(path):
            continue
        for r in pq.read_table(path).to_pylist():
            if n and len(want) >= n:
                return want
            want[r["uuid"]] = {"scale": r["scale"], "offs": r["offs"],
                               "max_dim_mm": r["max_dim_mm"],
                               "conv_code": r["cadquery_file"]}
    return want


def export_basics(want):
    """Write cadquery.py / step / stl / images / metadata / koor.json. Returns
    the list of uuids actually materialised."""
    import pyarrow.parquet as pq
    remaining = dict(want)
    done = []
    for f in sorted(glob.glob(ORIG_GLOB)):
        if not remaining:
            break
        t = pq.ParquetFile(f).read(
            columns=SCALAR_COLS + IMG_COLS + ["cadquery_file", "stl_file", "step_file"])
        idx = {u: i for i, u in enumerate(t.column("uuid").to_pylist())}
        hit = [u for u in list(remaining) if u in idx]
        if not hit:
            continue
        rows = t.to_pylist()
        for u in hit:
            r = rows[idx[u]]
            d = os.path.join(OUT, u)
            os.makedirs(d, exist_ok=True)
            code = _b(r["cadquery_file"])
            if isinstance(code, bytes):
                code = code.decode("utf-8", "replace")
            open(os.path.join(d, "cadquery.py"), "w", encoding="utf-8").write(code)
            if r["step_file"]:
                open(os.path.join(d, "model.step"), "wb").write(_b(r["step_file"]))
            if r["stl_file"]:
                open(os.path.join(d, "model.stl"), "wb").write(_b(r["stl_file"]))
            for i in range(8):
                v = r.get(f"image_{i}")
                if v:
                    open(os.path.join(d, f"image_{i}.png"), "wb").write(_b(v))
            meta = {k: r[k] for k in SCALAR_COLS}
            ops = meta.get("cadquery_ops_json")
            if isinstance(ops, (bytes, bytearray)):
                ops = bytes(ops).decode("utf-8", "replace")
            if isinstance(ops, str):
                try: ops = json.loads(ops)
                except Exception: ops = []
            if isinstance(ops, list):
                for op in ops:
                    if isinstance(op, dict) and "op_name" not in op:
                        fn = op.get("function", "")
                        op["op_name"] = fn.split(".")[-1] if fn else ""
            meta["cadquery_ops_json"] = ops
            json.dump(meta, open(os.path.join(d, "metadata.json"), "w",
                                 encoding="utf-8"), ensure_ascii=False, indent=2)
            kd = remaining.pop(u)
            json.dump(kd, open(os.path.join(d, "koor.json"), "w",
                               encoding="utf-8"), ensure_ascii=False, indent=2)
            done.append(u)
        print(f"  {os.path.basename(f)}: 基础模态写出 {len(hit)} (累计 {len(done)})", flush=True)
    if remaining:
        print(f"[warn] {len(remaining)} 个 uuid 未在原始 parquet 找到", flush=True)
    return done


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    want = load_converted(n)
    os.makedirs(OUT, exist_ok=True)
    print(f"目标 {len(want)} 个 uuid -> {OUT}", flush=True)

    uuids = export_basics(want)
    print(f"基础模态完成 {len(uuids)} 个; 生成工程图...", flush=True)

    # Redirect both pipeline modules' OUT to the isolated dir, then drive them.
    import make_drawings as md
    import augment_data as aug
    md.OUT = OUT
    aug.OUT = OUT

    dok = dfail = 0
    for u in uuids:
        try:
            md.process(u); dok += 1
        except Exception as e:
            dfail += 1; print(f"  [draw-fail] {u[:8]} {type(e).__name__}: {str(e)[:60]}", flush=True)
    print(f"工程图 ok={dok} fail={dfail}; 补点云/brep/描述...", flush=True)

    aok = afail = 0
    for u in uuids:
        try:
            aug.augment(u); aok += 1
        except Exception as e:
            afail += 1; print(f"  [aug-fail] {u[:8]} {type(e).__name__}: {str(e)[:60]}", flush=True)
    print(f"augment ok={aok} fail={afail}", flush=True)
    print(f"完成: {len(uuids)} 个 uuid 落地到 {OUT}", flush=True)


if __name__ == "__main__":
    main()
