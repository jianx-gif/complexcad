import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-11))
w1=cq.Workplane('XY',origin=(0,0,-16))
r=w0.workplane(offset=3/2).box(104,68,3).union(w1.sketch().segment((-100,-3),(-91,-3)).segment((-91,3)).segment((-100,3)).arc((-99,0),(-100,-3)).assemble().finalize().extrude(38))