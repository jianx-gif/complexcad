import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,75))
w1=cq.Workplane('ZX',origin=(0,-15,0))
r=w0.sketch().circle(25).circle(23,mode='s').finalize().extrude(-74).union(w0.workplane(offset=-17/2).cylinder(17,30)).union(w1.workplane(offset=36/2).moveTo(62,0).cylinder(36,22))
