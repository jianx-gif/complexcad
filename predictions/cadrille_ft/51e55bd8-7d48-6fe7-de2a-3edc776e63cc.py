import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,50,0))
w1=cq.Workplane('ZX',origin=(0,34,0))
r=w0.workplane(offset=-100/2).cylinder(100,38).union(w0.sketch().circle(59).circle(38,mode='s').finalize().extrude(-50)).union(w1.sketch().circle(100).circle(12,mode='s').finalize().extrude(16))