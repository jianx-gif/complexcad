import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-19,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(0,-1)]).circle(14).circle(10,mode='s').finalize().extrude(10).union(w1.sketch().arc((-90,-19),(-81,-28),(-70,-35)).segment((-70,-37)).segment((-67,-37)).arc((-1,-80),(67,-37)).segment((70,-37)).segment((70,-35)).arc((81,-28),(90,-19)).segment((81,-19)).arc((0,-80),(-81,-19)).close().assemble().finalize().extrude(-200))