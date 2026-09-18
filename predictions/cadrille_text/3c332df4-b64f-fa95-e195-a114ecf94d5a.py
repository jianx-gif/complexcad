import cadquery as cq
w0=cq.Workplane('XY',origin=(-67,-60,-100))
r=w0.sketch().segment((-67,57),(-67,60)).arc((-68,59),(-67,57)).assemble().reset().face(w0.sketch().arc((-66,56),(-64,55),(-62,56)).close().assemble()).reset().face(w0.sketch().segment((-66,61),(-62,61)).arc((-64,62),(-66,61)).assemble()).finalize().extrude(200)