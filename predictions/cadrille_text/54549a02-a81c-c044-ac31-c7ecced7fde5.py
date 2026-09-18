import cadquery as cq
w0=cq.Workplane('XY',origin=(-60,-60,-100))
r=w0.sketch().segment((-55,95),(-55,96)).arc((-59,93),(-54,95)).close().assemble().finalize().extrude(200)