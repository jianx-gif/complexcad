import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
r=w0.sketch().segment((-100,-16),(-98,-16)).arc((0,-100),(98,-16)).segment((100,-16)).segment((100,16)).segment((98,16)).arc((0,100),(-98,16)).segment((-100,16)).close().assemble().reset().face(w0.sketch().segment((-60,42),(-40,-60)).segment((60,-42)).segment((40,60)).close().assemble(),mode='s').finalize().extrude(-16)