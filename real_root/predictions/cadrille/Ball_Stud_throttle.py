import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,97,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((-30,-24),(0,-33),(30,-24)).close().assemble().reset().face(w0.sketch().segment((-30,24),(30,24)).arc((0,33),(-30,24)).assemble()).finalize().extrude(-191).union(w1.sketch().circle(33).circle(20,mode='s').finalize().extrude(-200))