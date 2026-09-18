import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((-97,48),(-97,50)).arc((-99,44),(-94,48)).close().assemble().finalize().extrude(100)