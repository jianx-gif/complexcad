import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-77,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().circle(100).circle(87,mode='s').finalize().extrude(175).union(w1.sketch().arc((-59,81),(53,-85),(-51,86)).arc((-51,78),(-59,81)).assemble().reset().face(w1.sketch().segment((-28,-70),(28,-70)).segment((28,-48)).arc((52,0),(28,48)).segment((28,70)).segment((-28,70)).segment((-28,48)).arc((-52,0),(-28,-48)).close().assemble(),mode='s').finalize().extrude(200))