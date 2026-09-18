import cadquery as cq
w0=cq.Workplane('XY',origin=(-62,-19,-100))
r=w0.sketch().segment((-62,19),(-62,21)).arc((-62,0),(-59,21)).segment((-59,19)).close().assemble().finalize().extrude(200)