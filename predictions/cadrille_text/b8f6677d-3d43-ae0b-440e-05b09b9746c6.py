import cadquery as cq
w0=cq.Workplane('XY',origin=(-50,0,-100))
r=w0.sketch().segment((-50,14),(-50,15)).arc((-50,0),(-46,14)).close().assemble().finalize().extrude(200)