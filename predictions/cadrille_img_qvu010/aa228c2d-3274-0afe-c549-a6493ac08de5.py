import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
w1=cq.Workplane('XY',origin=(0,0,-79))
r=w0.sketch().arc((-95,-18),(-73,-43),(-45,-59)).close().assemble().reset().face(w0.sketch().segment((4,59),(34,18)).arc((21,42),(4,59)).assemble()).finalize().extrude(200).union(w1.sketch().arc((-100,-12),(-89,12),(-74,33)).segment((-100,33)).close().assemble().finalize().extrude(179))