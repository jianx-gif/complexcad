"""Fig 4.2 (smooth solid | coarse mesh | normal-coloured point cloud) + Fig 4.3 (B-rep wireframe).
(a) is re-tessellated finely from STEP so curved faces look smooth; (b) is the coarse dataset STL
with visible wireframe; colours contrast: silver vs blue vs RGB normals."""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import sys, os, tempfile
import numpy as np, trimesh
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import cadquery as cq
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GCPnts import GCPnts_QuasiUniformDeflection
from OCP.TopoDS import TopoDS

uuid = sys.argv[1]
OUTPNG = sys.argv[2] if len(sys.argv) > 2 else None   # preview path; None -> thesis bilder
BILD = _ROOT + '/overleaf_thesis/bilder'
ROOT = f"{_ROOT}/output/{uuid}"
ELEV, AZIM = 24, -58
LIM = 0.62
VIEW = np.array([np.cos(np.radians(AZIM))*np.cos(np.radians(ELEV)),
                 np.sin(np.radians(AZIM))*np.cos(np.radians(ELEV)),
                 np.sin(np.radians(ELEV))])
L1 = np.array([0.45,-0.55,0.7]); L1/=np.linalg.norm(L1)
L2 = np.array([-0.7,0.4,0.25]); L2/=np.linalg.norm(L2)

def setup(ax, title):
    ax.set_xlim(-LIM,LIM); ax.set_ylim(-LIM,LIM); ax.set_zlim(-LIM,LIM)
    ax.set_box_aspect((1,1,1)); ax.view_init(elev=ELEV, azim=AZIM); ax.set_axis_off()
    if title: ax.set_title(title, fontsize=12, pad=6)

def shade(tris_v, nrm, base_hex, sat=0.55, amb=0.30):
    base = np.array(mcolors.to_rgb(base_hex)); base = sat*base + (1-sat)
    it = np.clip(amb + 0.60*np.clip(nrm@L1,0,1) + 0.24*np.clip(nrm@L2,0,1), 0, 1)
    return np.clip(base[None,:]*it[:,None], 0, 1)

def depth_sort(tris, nrm, cull=True):
    if cull:
        keep = (nrm @ VIEW) > -0.03   # backface culling: closed solid, back faces never visible
        tris, nrm = tris[keep], nrm[keep]
    fo = np.argsort(tris.mean(1) @ VIEW)
    return tris[fo], nrm[fo]

# ---- geometry: coarse dataset STL + fine STEP tessellation ----
mc = trimesh.load(f"{ROOT}/model.stl", force="mesh")
c0 = mc.vertices.mean(0); s = float(np.abs(mc.vertices - c0).max()) + 1e-9

w = cq.importers.importStep(f"{ROOT}/model.step")
tmp = os.path.join(tempfile.gettempdir(), f"_fine_{uuid[:8]}.stl")
cq.exporters.export(w, tmp, tolerance=0.03, angularTolerance=0.08)
mf = trimesh.load(tmp, force="mesh")

Vf = (mf.vertices - c0)/s; TF, NF = depth_sort(Vf[mf.faces], mf.face_normals)
Vc = (mc.vertices - c0)/s; TC, NC = depth_sort(Vc[mc.faces], mc.face_normals)

pc = np.load(f"{ROOT}/point_cloud.npy")
P = (pc[:,:3] - c0)/s; N = pc[:,3:6]
rgb = np.clip((N + 1.0)/2.0, 0, 1)
o = np.argsort(P @ VIEW)

# ---- Fig 4.2 ----
fig = plt.figure(figsize=(15, 5.6))
ax = fig.add_subplot(131, projection="3d")
fcA = shade(TF, NF, "#B9BEC7", sat=0.75, amb=0.34)
ax.add_collection3d(Poly3DCollection(TF, facecolors=fcA, edgecolors=fcA, linewidths=0.3))
setup(ax, "(a) Executed parametric solid $S$ (exact B-rep, smooth)")
ax = fig.add_subplot(132, projection="3d")
ax.add_collection3d(Poly3DCollection(TC, facecolors=shade(TC, NC, "#4C9BE8"), edgecolor=(0.06,0.14,0.28,0.65), linewidths=0.4))
setup(ax, "(b) Tessellation of $\partial S$ (%d triangles)" % len(mc.faces))
ax = fig.add_subplot(133, projection="3d")
ax.scatter(P[o,0], P[o,1], P[o,2], c=rgb[o], s=6.5, depthshade=False, linewidths=0.15, edgecolors=(0,0,0,0.35))
setup(ax, "(c) %d sampled points, coloured by normal (RGB=$n_x n_y n_z$)" % len(P))
out42 = OUTPNG or f"{BILD}/pointcloud_sampling.png"
fig.subplots_adjust(left=0.01,right=0.99,top=0.9,bottom=0.02,wspace=0.0)
fig.savefig(out42, dpi=180, bbox_inches="tight", pad_inches=0.05); plt.close(fig)
print("42:", out42)

# ---- Fig 4.3 (only when not preview) ----
if not OUTPNG:
    shape = w.val().wrapped
    segs = []
    exp = TopExp_Explorer(shape, TopAbs_EDGE)
    while exp.More():
        e = TopoDS.Edge_s(exp.Current())
        try:
            c = BRepAdaptor_Curve(e); dd = GCPnts_QuasiUniformDeflection(c, 0.05)
            pts = np.array([[c.Value(dd.Parameter(i)).X(), c.Value(dd.Parameter(i)).Y(), c.Value(dd.Parameter(i)).Z()] for i in range(1, dd.NbPoints()+1)])
            if len(pts) > 1: segs.append(np.asarray((pts - c0)/s, dtype=float))
        except Exception: pass
        exp.Next()
    fig = plt.figure(figsize=(7, 7)); ax = fig.add_subplot(111, projection="3d")
    ax.add_collection3d(Poly3DCollection(TF, facecolors=np.clip(shade(TF,NF,"#9FB2CC",sat=0.6,amb=0.5)*0.3+0.68,0,1), edgecolor="none", alpha=0.12))
    lc = Line3DCollection(segs, colors="#0c2450", linewidths=1.5); ax.add_collection3d(lc, autolim=False)
    setup(ax, "")
    fig.subplots_adjust(left=0,right=1,top=1,bottom=0)
    fig.savefig(f"{BILD}/example_brep.png", dpi=180, bbox_inches="tight", pad_inches=0.05); plt.close(fig)
    print("43: example_brep.png edges:", len(segs))
