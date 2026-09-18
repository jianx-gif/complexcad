import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,49,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(0,34)]).circle(12).circle(10,mode='s').finalize().extrude(-107).union(w1.sketch().segment((-100,14),(-89,14)).arc((0,-71),(89,14)).segment((100,14)).segment((100,22)).segment((-89,22)).arc((0,71),(89,23)).segment((100,23)).segment((100,31)).arc((-1,71),(-100,31)).close().assemble().finalize().extrude(-183))