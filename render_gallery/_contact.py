"""Contact sheet: shaded solid previews for candidate parts."""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import sys, os, tempfile
import numpy as np, trimesh
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import cadquery as cq

ELEV, AZIM = 24, -58
VIEW = np.array([np.cos(np.radians(AZIM))*np.cos(np.radians(ELEV)),
                 np.sin(np.radians(AZIM))*np.cos(np.radians(ELEV)), np.sin(np.radians(ELEV))])
L1 = np.array([0.45,-0.55,0.7]); L1/=np.linalg.norm(L1)
L2 = np.array([-0.7,0.4,0.25]); L2/=np.linalg.norm(L2)
uuids = sys.argv[1:]
n = len(uuids); cols = 3; rows = (n+cols-1)//cols
fig = plt.figure(figsize=(4.6*cols, 4.6*rows))
for i, u in enumerate(uuids):
    ax = fig.add_subplot(rows, cols, i+1, projection="3d")
    try:
        w = cq.importers.importStep(f"{_ROOT}/output/{u}/model.step")
        tmp = os.path.join(tempfile.gettempdir(), f"_cs_{u[:8]}.stl")
        cq.exporters.export(w, tmp, tolerance=0.05, angularTolerance=0.12)
        m = trimesh.load(tmp, force="mesh")
        c0 = m.vertices.mean(0); s = float(np.abs(m.vertices-c0).max())+1e-9
        V = (m.vertices-c0)/s; tris = V[m.faces]; nrm = m.face_normals
        keep = (nrm @ VIEW) > -0.03; tris, nrm = tris[keep], nrm[keep]
        fo = np.argsort(tris.mean(1) @ VIEW); tris, nrm = tris[fo], nrm[fo]
        base = np.array(mcolors.to_rgb("#B9BEC7")); base = 0.75*base + 0.25
        it = np.clip(0.34 + 0.60*np.clip(nrm@L1,0,1) + 0.24*np.clip(nrm@L2,0,1),0,1)
        fc = np.clip(base[None,:]*it[:,None],0,1)
        ax.add_collection3d(Poly3DCollection(tris, facecolors=fc, edgecolors=fc, linewidths=0.3))
    except Exception as e:
        ax.text2D(0.5,0.5,str(e)[:30],ha="center",transform=ax.transAxes)
    ax.set_xlim(-0.62,0.62); ax.set_ylim(-0.62,0.62); ax.set_zlim(-0.62,0.62)
    ax.set_box_aspect((1,1,1)); ax.view_init(elev=ELEV,azim=AZIM); ax.set_axis_off()
    ax.set_title(u[:8], fontsize=10)
fig.tight_layout()
fig.savefig(_ROOT + '/render_gallery/_contact.png', dpi=110, bbox_inches="tight")
print("SAVED _contact.png")
