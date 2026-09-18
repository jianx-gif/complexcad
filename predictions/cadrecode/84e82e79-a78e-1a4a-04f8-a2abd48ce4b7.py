import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,16))
r=w0.sketch().circle(23).circle(21,mode='s').finalize().extrude(-32).union(w0.workplane(offset=-27/2).cylinder(27,87)).union(w0.workplane(offset=-17/2).cylinder(17,100))