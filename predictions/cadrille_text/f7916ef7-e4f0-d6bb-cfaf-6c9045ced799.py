import cadquery as cq
w0=cq.Workplane('XY',origin=(-1,-19,-100))
r=w0.sketch().segment((-1,-1),(1,-1)).segment((1,1)).segment((0,1)).segment((0,3)).segment((1,3)).segment((1,19)).arc((0,18),(-1,19)).close().assemble().finalize().extrude(200)