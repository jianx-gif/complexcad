import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-11,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().push([(0,16)]).circle(7).circle(3,mode='s').finalize().extrude(-59).union(w1.sketch().segment((-89,-29),(-63,-29)).arc((-16,-74),(42,-50)).segment((89,-50)).segment((89,50)).segment((38,50)).arc((-15,79),(-69,50)).segment((-89,50)).close().assemble().push([(0,1)]).circle(77,mode='s').finalize().extrude(200))