"""预处理单个真实STL: python prep_one.py <src> <dst>
大网格先抽稀(>80k面→60k)再补洞(防止巨网格close_holes卡死), 输出水密性状态。"""
import sys
import pymeshlab
import trimesh

src, dst = sys.argv[1], sys.argv[2]
ms = pymeshlab.MeshSet()
ms.load_new_mesh(src)
n0 = ms.current_mesh().face_number()
if n0 > 80000:
    ms.meshing_decimation_quadric_edge_collapse(targetfacenum=60000,
                                                preservenormal=True)
ms.meshing_remove_duplicate_faces()
ms.meshing_remove_unreferenced_vertices()
try:
    ms.meshing_merge_close_vertices()
except Exception:
    pass
try:
    ms.meshing_close_holes(maxholesize=400)
except Exception as e:
    print("close_holes warn:", str(e)[:60])
ms.save_current_mesh(dst)
m = trimesh.load(dst, force="mesh")
print("PREP", "faces", n0, "->", len(m.faces),
      "watertight" if m.is_watertight else "OPEN")
