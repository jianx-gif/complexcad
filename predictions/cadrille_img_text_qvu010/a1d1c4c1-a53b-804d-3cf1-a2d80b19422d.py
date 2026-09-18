import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,35,0))
r=w0.sketch().segment((-1,-71),(1,-71)).segment((1,-69)).arc((69,0),(1,69)).segment((1,71)).segment((-1,71)).segment((-1,69)).arc((-69,0),(-1,-69)).close().assemble().finalize().extrude(167).union(w1.sketch().push([(0,-1)]).circle(99).circle(97,mode='s').finalize().extrude(-70))