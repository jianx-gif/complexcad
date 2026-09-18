import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((93,-43),(100,-19)).segment((93,-19)).close().assemble().finalize().extrude(100)