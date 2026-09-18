import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-89,0))
r=w0.sketch().circle(100).circle(89,mode='s').circle(62).finalize().extrude(189).union(w0.workplane(offset=189/2).box(12,186,189))