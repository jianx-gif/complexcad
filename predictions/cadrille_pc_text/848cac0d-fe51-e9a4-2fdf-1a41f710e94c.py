import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-32))
w1=cq.Workplane('XY',origin=(0,0,-25))
r=w0.sketch().segment((-94,-28),(-94,28)).arc((-100,0),(-94,-28)).assemble().reset().face(w0.sketch().arc((-88,-44),(0,-100),(88,-44)).segment((36,-44)).arc((47,0),(36,44)).segment((88,44)).arc((0,100),(-88,44)).segment((-36,44)).arc((-47,0),(-36,-44)).close().assemble()).reset().face(w0.sketch().arc((94,-28),(100,0),(94,28)).close().assemble()).finalize().extrude(78).union(w1.sketch().circle(100).circle(93,mode='s').finalize().extrude(71))