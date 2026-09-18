import cadquery as cq
w0=cq.Workplane('XY',origin=(-22,-22,-100))
r=w0.sketch().segment((-22,-16),(-22,16)).arc((-25,0),(-22,-16)).assemble().reset().face(w0.sketch().arc((22,-16),(25,0),(22,16)).close().assemble()).finalize().extrude(200)