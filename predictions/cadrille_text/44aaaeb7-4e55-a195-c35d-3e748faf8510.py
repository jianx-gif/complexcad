import cadquery as cq
w0=cq.Workplane('ZX',origin=(-100,100,0))
w1=cq.Workplane('ZX',origin=(-40,100,0))
r=w0.sketch().face(w0.sketch().segment((-53,93),(-52,93)).segment((-52,94)).close().assemble()).finalize().extrude(-200).union(w1.sketch().face(w1.sketch().segment((0,0),(0,80)).arc((-33,40),(0,0)).assemble()).finalize().extrude(-200))