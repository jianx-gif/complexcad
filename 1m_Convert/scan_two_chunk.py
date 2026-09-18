"""候选池扫描 worker(子进程, 带 wall-clock 超时由父进程控制): 扫描数据集中
[start, start+count) 区间的件, 对每个件检孔 + 平面对接端判定, 把"有平面对接孔"的
件以 JSON 行打印到 stdout(一行一件)。父进程 batch_two 用子进程 + 超时调用本脚本,
这样某个病态零件让 cylinder_holes/平面检测卡死时, 整个 chunk 子进程被杀, 父进程
跳过该 chunk 继续, 不会拖死整池扫描。

用法: python -X utf8 scan_two_chunk.py <start> <count>
输出: 每行 {"uuid":..., "holes":[...]} ; 末行打印 "__DONE__ <scanned>"
"""
import sys, os, glob, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import pyarrow.parquet as pq
import assemble_fasteners as af
import assemble_two as a2

import dataset_source


def _entry(shape):
    td = a2._topods(shape)
    holes = af.cylinder_holes(shape)
    out = []
    for h in holes:
        m = af.match_screw_size(2 * h[0])
        if m is None:
            continue
        size, nominal = m
        axis = a2._axis_to_z(h[1])
        eh = a2._orient_hole_to_axis(h, axis)
        ep = a2.hole_plane_ends(td, eh)
        hi_p = ep["hi"][0]; lo_p = ep["lo"][0]
        if not (hi_p or lo_p):
            continue
        out.append({"size": size, "nominal": float(nominal), "r": float(h[0]),
                    "hi": bool(hi_p), "lo": bool(lo_p),
                    "p": [float(x) for x in h[2]], "a": [float(x) for x in axis]})
    return out


def main():
    start = int(sys.argv[1]); count = int(sys.argv[2])
    files = dataset_source.parquet_files()
    idx = 0
    scanned = 0
    for f in files:
        pf = pq.ParquetFile(f)
        nrows = pf.metadata.num_rows
        if idx + nrows <= start:
            idx += nrows
            continue
        for rg in range(pf.num_row_groups):
            rows = pf.read_row_group(rg, columns=["uuid", "cadquery_file"]).to_pylist()
            for row in rows:
                if idx < start:
                    idx += 1
                    continue
                if scanned >= count:
                    print("__DONE__ %d" % scanned, flush=True)
                    return
                idx += 1
                scanned += 1
                try:
                    shape, _ = a2.exec_part(row["cadquery_file"])
                    if shape is None:
                        continue
                    holes = _entry(shape)
                    if holes:
                        print(json.dumps({"uuid": row["uuid"], "holes": holes}),
                              flush=True)
                except Exception:
                    pass
    print("__DONE__ %d" % scanned, flush=True)


if __name__ == "__main__":
    main()
