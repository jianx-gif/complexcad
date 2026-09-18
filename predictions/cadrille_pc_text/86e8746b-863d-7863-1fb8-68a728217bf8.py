import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,13,0))
w1=cq.Workplane('XY',origin=(0,0,87))
r=w0.sketch().circle(100).circle(83,mode='s').finalize().extrude(-27).union(w1.workplane(offset=-149/2).moveTo(0,-1).cylinder(149,28))