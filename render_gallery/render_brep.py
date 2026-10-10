"""B-rep wireframe render (edges of the exact boundary representation) for fig:brep."""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import sys, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import cadquery as cq
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GCPnts import GCPnts_QuasiUniformDeflection
from OCP.TopoDS import TopoDS

uuid, out = sys.argv[1], sys.argv[2]
shape = cq.importers.importStep(f"{_ROOT}/output/{uuid}/model.step").val().wrapped
segs = []
exp = TopExp_Explorer(shape, TopAbs_EDGE)
while exp.More():
    e = TopoDS.Edge_s(exp.Current())
    try:
        c = BRepAdaptor_Curve(e); d = GCPnts_QuasiUniformDeflection(c, 0.05)
        pts = [c.Value(d.Parameter(i)) for i in range(1, d.NbPoints()+1)]
        P = np.array([[p.X(), p.Y(), p.Z()] for p in pts])
        if len(P) > 1: segs.append(P)
    except Exception: pass
    exp.Next()
allp = np.vstack(segs); c0 = allp.mean(0); s = float(np.abs(allp - c0).max()) + 1e-9
segs = [np.asarray((P - c0)/s, dtype=float) for P in segs]
fig = plt.figure(figsize=(6.5, 6.5)); ax = fig.add_subplot(111, projection="3d")
lc = Line3DCollection(segs, colors="#1f3a5f", linewidths=0.9); ax.add_collection3d(lc, autolim=False)
ax.set_xlim(-1,1); ax.set_ylim(-1,1); ax.set_zlim(-1,1); ax.set_box_aspect((1,1,1))
ax.view_init(elev=24, azim=-58); ax.set_axis_off()
fig.tight_layout(); fig.savefig(out, dpi=170, bbox_inches="tight"); print("SAVED", out, "edges:", len(segs))
