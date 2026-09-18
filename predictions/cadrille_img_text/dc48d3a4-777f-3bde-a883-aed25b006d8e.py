import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
w1=cq.Workplane('ZX',origin=(0,-67,0))
r=w0.sketch().arc((-33,-70),(-22,-62),(-12,-54)).arc((-19,-49),(-24,-43)).close().assemble().reset().face(w0.sketch().arc((12,54),(22,49),(27,43)).arc((33,40),(38,36)).arc((30,51),(12,54)).assemble()).finalize().extrude(200).union(w1.sketch().push([(10,14)]).circle(66).circle(62,mode='s').finalize().extrude(94))