import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-71))
r=w0.sketch().segment((-100,31),(-99,28)).segment((-99,32)).close().assemble().reset().face(w0.sketch().segment((-98,32),(-97,32)).segment((-97,33)).close().assemble()).reset().face(w0.sketch().segment((97,-33),(98,-32)).segment((97,-32)).close().assemble()).finalize().extrude(142)