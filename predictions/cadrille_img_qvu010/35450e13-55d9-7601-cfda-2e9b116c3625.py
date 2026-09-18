import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,-20,0))
r=w0.sketch().segment((-95,-19),(-79,-19)).arc((-82,0),(-79,19)).segment((-95,19)).close().assemble().reset().face(w0.sketch().segment((-68,-56),(29,-89)).segment((68,24)).segment((-29,57)).close().assemble()).push([(0,-16)]).circle(39,mode='s').finalize().extrude(200).union(w1.sketch().push([(0,10)]).rect(200,170).circle(89,mode='s').finalize().extrude(-11))