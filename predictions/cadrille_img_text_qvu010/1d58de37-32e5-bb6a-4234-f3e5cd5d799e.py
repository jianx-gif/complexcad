import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,-2,0))
r=w0.sketch().arc((-90,-24),(-89,-25),(-87,-27)).segment((58,-27)).arc((56,-25),(55,-24)).close().assemble().reset().face(w0.sketch().arc((-90,24),(19,8),(58,-86)).arc((60,-79),(62,-72)).arc((20,84),(-90,-24)).assemble()).finalize().extrude(200).union(w1.sketch().arc((-100,-1),(-89,33),(-100,66)).close().assemble().finalize().extrude(-2))