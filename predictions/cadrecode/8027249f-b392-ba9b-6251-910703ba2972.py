import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-1))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.workplane(offset=-11/2).moveTo(0,-13).box(174,66,11).union(w1.sketch().segment((-1,-7),(12,-7)).segment((12,7)).segment((-1,7)).segment((-1,-1)).arc((5,-3),(-1,-4)).close().assemble().finalize().extrude(-200))