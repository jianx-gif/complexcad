import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,11))
w1=cq.Workplane('XY',origin=(0,0,15))
r=w0.workplane(offset=-44/2).cylinder(44,100).union(w1.sketch().circle(88).circle(82,mode='s').finalize().extrude(18))