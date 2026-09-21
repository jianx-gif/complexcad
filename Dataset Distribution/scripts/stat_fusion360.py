"""
统计 Fusion360 Gallery reconstruction 子集的操作分布。

数据获取（官方）：
  仓库 https://github.com/AutodeskAILab/Fusion360GalleryDataset
  reconstruction 数据需从官方说明里的链接下载 r1.0.1（一堆 *.json，每个是一个设计序列）。
  下载解压后，把所有 json 所在目录传给 --dir。

每个 reconstruction json 的结构（官方 schema）：
  { "entities": {...}, "sequence": [ {"type":"Sketch"/"ExtrudeFeature", ...}, ... ],
    "properties": {...} }
  - sketch 实体里 curves 有 "Line3D"/"Arc3D"/"Circle3D"/"SplineCurve" 等
  - ExtrudeFeature 有 "operation": "NewBodyFeatureOperation"/"JoinFeatureOperation"/
    "CutFeatureOperation"/"IntersectFeatureOperation"

用法:
    python stat_fusion360.py --dir "E:\path\to\reconstruction"  [--limit 1725]
"""
import argparse, json, os, glob
from collections import Counter

SKETCH_CURVE_MAP = {
    "Line3D": "line", "SketchLine": "line",
    "Arc3D": "arc", "SketchArc": "arc",
    "Circle3D": "circle", "SketchCircle": "circle",
    "SketchFittedSpline": "spline", "SketchFixedSpline": "spline", "SplineCurve": "spline",
    "SketchEllipse": "ellipse", "SketchConicCurve": "conic", "SketchEllipticalArc": "ellipticalArc",
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="包含 reconstruction *.json 的目录")
    ap.add_argument("--limit", type=int, default=0, help="0=全部")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.dir, "**", "*.json"), recursive=True))
    if args.limit:
        files = files[:args.limit]
    print(f"[*] 找到 {len(files)} 个 json")

    n = 0
    op_type_counter = Counter()        # sequence 里各 entity type
    extrude_bool = Counter()           # 拉伸的布尔类型
    curve_presence = Counter()         # 含某图元的模型数
    seq_len_list = []
    sketch_count_list = []

    for fp in files:
        try:
            with open(fp, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue
        if "timeline" not in data or "entities" not in data:
            continue                      # 跳过划分文件等非模型 json（如 train_test.json）
        n += 1
        entities = data.get("entities", {})
        # 1) 操作类型：按 timeline（每个建模步骤一条，Sketch / ExtrudeFeature）计数。
        #    注意 "sequence" 字段是逐曲线/逐轮廓的细粒度步骤（每个 Sketch 会被展开成多条），
        #    用它统计会把 Sketch 数放大约 7 倍（2026-09-21 更正：153456 -> 21557）。
        timeline = data.get("timeline", [])
        seq_len_list.append(len(timeline))
        n_sketch = 0
        for step in timeline:
            ent = entities.get(step.get("entity", ""), {})
            t = ent.get("type", "") if isinstance(ent, dict) else ""
            op_type_counter[t] += 1
            if "Sketch" in t:
                n_sketch += 1
        # 2) 遍历 entities：图元 type 在 Sketch.curves；布尔 type 在 ExtrudeFeature.operation
        model_curves = set()
        for ent in entities.values():
            if not isinstance(ent, dict):
                continue
            etype = ent.get("type", "")
            if etype == "Sketch":
                curves = ent.get("curves", {})
                if isinstance(curves, dict):
                    for c in curves.values():
                        mapped = SKETCH_CURVE_MAP.get(c.get("type", "") if isinstance(c, dict) else "")
                        if mapped:
                            model_curves.add(mapped)
            elif etype == "ExtrudeFeature":
                op = ent.get("operation", "")
                if op:
                    extrude_bool[op] += 1
        for c in model_curves:
            curve_presence[c] += 1
        sketch_count_list.append(n_sketch)

    def stats(lst):
        if not lst: return {}
        s = sorted(lst)
        return {"min": s[0], "median": s[len(s)//2], "max": s[-1],
                "mean": round(sum(s)/len(s), 2)}

    result = {
        "dataset": "Fusion360 Gallery (reconstruction)",
        "n_samples": n,
        "operation_type_counts": dict(op_type_counter.most_common()),
        "extrude_boolean_counts": dict(extrude_bool.most_common()),
        "sketch_curve_presence_count": dict(curve_presence.most_common()),
        "sketch_curve_presence_pct": {k: round(100*v/n, 2) for k, v in curve_presence.most_common()} if n else {},
        "sequence_length_stats": stats(seq_len_list),
        "sketch_per_model_stats": stats(sketch_count_list),
        "note": "复杂操作(Loft/Revolve/Sweep/Chamfer/Fillet)若在 operation_type_counts 中缺失，即为该数据集不含的直接证据",
    }
    outdir = os.path.join(os.path.dirname(__file__), "out")
    os.makedirs(outdir, exist_ok=True)
    outpath = args.out or os.path.join(outdir, "fusion360_recon_stats.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("="*60)
    print(f"Fusion360 reconstruction — {n} 个模型")
    print("="*60)
    print("[sequence 中各操作类型计数]")
    for k, v in op_type_counter.most_common():
        print(f"   {k:30s} {v}")
    print("[拉伸布尔类型]", dict(extrude_bool))
    print("[图元覆盖率%]", result["sketch_curve_presence_pct"])
    print("[序列长度]", result["sequence_length_stats"])
    print(f"[+] 写入 {outpath}")

if __name__ == "__main__":
    main()
