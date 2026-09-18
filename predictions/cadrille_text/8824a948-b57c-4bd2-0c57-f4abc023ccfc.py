import cadquery as cq
w0=cq.Workplane('XY',origin=(-67,-100,-67))
r=w0.sketch().segment((-67,100),(-32,100)).arc((-49,98),(-67,100)).assemble().reset().face(w0.sketch().arc((32,-67),(67,-10),(32,47)).close().assemble()).finalize().extrude(133)