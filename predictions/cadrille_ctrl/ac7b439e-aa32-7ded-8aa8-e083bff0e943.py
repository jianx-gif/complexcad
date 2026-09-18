import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,65))
w1=cq.Workplane('XY',origin=(0,0,93))
r=w0.sketch().segment((-15,-9),(13,-10)).segment((15,9)).segment((-15,10)).close().assemble().finalize().extrude(-65).union(w0.workplane(offset=15/2).cylinder(15,20)).union(w1.workplane(offset=-14/2).cylinder(14,8))
