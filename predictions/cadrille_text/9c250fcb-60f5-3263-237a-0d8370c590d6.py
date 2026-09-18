import cadquery as cq
w0=cq.Workplane('XY',origin=(-67,-100,-67))
r=w0.sketch().segment((-67,100),(-66,98)).segment((-66,100)).close().assemble().reset().face(w0.sketch().segment((66,-100),(67,-100)).segment((66,-98)).close().assemble()).finalize().extrude(134)