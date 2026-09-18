"""从 cadfit_repro/grabcad_run/*.stl 采样 8192 点+法向 ->
real_root/output/<name>/point_cloud.npy (与 ComplexCAD 同格式), 并写 names.txt。"""
import os, glob
import numpy as np
import trimesh

SRC = "E:/3005/data/cadfit_repro/grabcad_run"
ROOT = "E:/3005/data/real_root"

names = []
for f in sorted(glob.glob(os.path.join(SRC, "*.stl"))):
    n = os.path.splitext(os.path.basename(f))[0]
    m = trimesh.load(f, force="mesh")
    pts, fid = trimesh.sample.sample_surface(m, 8192)
    normals = m.face_normals[fid]
    arr = np.hstack([pts, normals]).astype(np.float32)
    d = os.path.join(ROOT, "output", n)
    os.makedirs(d, exist_ok=True)
    np.save(os.path.join(d, "point_cloud.npy"), arr)
    names.append(n)
    print("PC", n, arr.shape)

os.makedirs(os.path.join(ROOT, "predictions"), exist_ok=True)
with open(os.path.join(ROOT, "names.txt"), "w") as fh:
    fh.write("\n".join(names))
print("names:", len(names))
