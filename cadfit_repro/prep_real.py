"""预处理 stl_data 真实件 -> cadfit_repro/grabcad_in/
- 去重(大小写glob重复) + 安全文件名(无空格/非ASCII)
- pymeshlab 修复非水密(合并近点/去重面/补洞)
- >60k 面抽稀到 50k (与 CADFit image_to_cad 流程一致)
- 输出后用 trimesh 验证水密性
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, glob, re, sys
import pymeshlab
import trimesh

SRC = _ROOT + '/stl_data'
DST = _ROOT + '/cadfit_repro/grabcad_in'
os.makedirs(DST, exist_ok=True)

# 收集去重(Windows大小写不敏感造成 *.stl/*.STL 双计)
files = {}
for f in glob.glob(os.path.join(SRC, "*.stl")) + glob.glob(os.path.join(SRC, "*.STL")):
    files[os.path.normcase(f)] = f
files = sorted(files.values())
print("唯一STL:", len(files))


def safe_name(p):
    b = os.path.splitext(os.path.basename(p))[0]
    b = re.sub(r"[^A-Za-z0-9_-]+", "_", b).strip("_")[:40]
    return b or "part"


seen = set()
report = []
for f in files:
    name = safe_name(f)
    while name in seen:
        name += "_x"
    seen.add(name)
    out = os.path.join(DST, name + ".stl")
    try:
        ms = pymeshlab.MeshSet()
        ms.load_new_mesh(f)
        n0 = ms.current_mesh().face_number()
        # 基本清理
        ms.meshing_remove_duplicate_faces()
        ms.meshing_remove_duplicate_vertices()
        ms.meshing_merge_close_vertices()
        ms.meshing_remove_unreferenced_vertices()
        # 补洞(非水密修复)
        try:
            ms.meshing_close_holes(maxholesize=400)
        except Exception:
            pass
        # 抽稀
        n1 = ms.current_mesh().face_number()
        if n1 > 60000:
            ms.meshing_decimation_quadric_edge_collapse(targetfacenum=50000,
                                                        preservenormal=True)
        ms.save_current_mesh(out)
        m = trimesh.load(out, force="mesh")
        wt = "OK-watertight" if m.is_watertight else "STILL-OPEN"
        report.append((name, n0, len(m.faces), wt))
        print("%-42s %7d->%6d  %s" % (name, n0, len(m.faces), wt))
    except Exception as e:
        report.append((name, -1, -1, "ERR " + str(e)[:40]))
        print(name, "ERR", str(e)[:60])

good = [r for r in report if r[3] == "OK-watertight"]
print("\n水密可用: %d / %d" % (len(good), len(report)))
