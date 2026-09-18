import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,89,0))
r=w0.workplane(offset=-178/2).moveTo(0,-66.5).box(18,67,178).union(w0.sketch().segment((-9,-100),(9,-100)).segment((9,-11)).segment((-2,-11)).segment((-2,33)).segment((9,33)).segment((9,100)).segment((-9,100)).close().assemble().finalize().extrude(-67))