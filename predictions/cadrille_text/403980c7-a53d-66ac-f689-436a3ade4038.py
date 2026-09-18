import cadquery as cq
w0=cq.Workplane('XY',origin=(-60,-50,-100))
r=w0.sketch().segment((-50,19),(29,-58)).segment((50,-37)).segment((-29,39)).close().assemble().finalize().extrude(200)