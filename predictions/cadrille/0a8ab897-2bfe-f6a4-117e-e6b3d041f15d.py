import cadquery as cq
w0=cq.Workplane('YZ',origin=(-60,0,0))
w1=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().segment((-6,-9),(6,-9)).segment((6,9)).segment((-6,9)).segment((-6,5)).arc((-4,3),(-6,1)).close().assemble().finalize().extrude(119).union(w1.sketch().segment((-25,-4),(25,-4)).arc((22,5),(18,9)).segment((-18,9)).arc((-22,4),(-25,-2)).close().assemble().push([(16,1)]).circle(3,mode='s').finalize().extrude(200))