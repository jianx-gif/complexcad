import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
w1=cq.Workplane('ZX',origin=(0,-77,0))
r=w0.sketch().segment((-15,-16),(-1,-10)).arc((3,2),(12,10)).segment((15,16)).arc((-5,7),(-15,-12)).close().assemble().finalize().extrude(200).union(w1.sketch().circle(88).reset().face(w1.sketch().segment((-73,-30),(-60,-30)).arc((-4,-73),(53,-30)).segment((66,-30)).segment((66,30)).segment((53,30)).arc((-4,73),(-60,30)).segment((-73,30)).close().assemble(),mode='s').finalize().extrude(123))