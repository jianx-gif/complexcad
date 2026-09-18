import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-34,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(0,12)]).circle(12).circle(9,mode='s').finalize().extrude(10).union(w0.sketch().push([(0,12)]).circle(17).circle(12,mode='s').finalize().extrude(69)).union(w1.sketch().arc((-100,-33),(0,-81),(100,-33)).segment((100,-33),(100,33)).segment((100,33),(100,81)).arc((0,68),(-100,81)).close().assemble().finalize().extrude(-200))