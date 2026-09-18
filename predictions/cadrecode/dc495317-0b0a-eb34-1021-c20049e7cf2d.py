import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
w1=cq.Workplane('ZX',origin=(0,-95,0))
r=w0.sketch().circle(37).circle(33,mode='s').finalize().extrude(100).union(w0.sketch().circle(25).circle(20,mode='s').finalize().extrude(200)).union(w1.workplane(offset=190/2).cylinder(190,25))