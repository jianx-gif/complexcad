import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-83))
r=w0.workplane(offset=-17/2).cylinder(17,82).union(w0.sketch().circle(73).circle(50,mode='s').finalize().extrude(183))