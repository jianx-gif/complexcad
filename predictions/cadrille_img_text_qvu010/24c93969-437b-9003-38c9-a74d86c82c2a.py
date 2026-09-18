import cadquery as cq
w0=cq.Workplane('YZ',origin=(43,0,0))
w1=cq.Workplane('ZX',origin=(0,38,0))
r=w0.sketch().segment((-72,-18),(-72,18)).arc((-75,0),(-72,-18)).assemble().reset().face(w0.sketch().arc((-60,-57),(0,-85),(60,-57)).segment((28,-57)).arc((42,-28),(28,2)).segment((60,2)).arc((0,30),(-60,2)).segment((-28,2)).arc((-42,-28),(-28,-57)).close().assemble()).reset().face(w0.sketch().arc((72,-18),(75,0),(72,18)).close().assemble()).finalize().extrude(-143).union(w1.sketch().circle(100).circle(99,mode='s').finalize().extrude(-78))