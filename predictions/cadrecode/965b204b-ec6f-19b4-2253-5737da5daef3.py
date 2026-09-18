import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
w1=cq.Workplane('ZX',origin=(0,-1,0))
r=w0.sketch().segment((-57,-7),(29,-7)).arc((23,0),(21,2)).segment((-57,2)).close().assemble().finalize().extrude(-200).union(w1.workplane(offset=58/2).moveTo(2,57).box(10,28,58))