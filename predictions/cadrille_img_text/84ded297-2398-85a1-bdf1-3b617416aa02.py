import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-38,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(74,0)]).circle(14).circle(10,mode='s').finalize().extrude(122).union(w1.sketch().arc((-90,-40),(0,-68),(90,-40)).segment((90,-38)).arc((88,-23),(90,-8)).segment((90,-6)).arc((0,68),(-90,-6)).segment((-90,-8)).arc((-92,-23),(-90,-38)).close().assemble().finalize().extrude(-200))