import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,0,-100))
r=w0.sketch().segment((-53,17),(-53,18)).arc((-52,10),(-49,17)).close().assemble().finalize().extrude(200)