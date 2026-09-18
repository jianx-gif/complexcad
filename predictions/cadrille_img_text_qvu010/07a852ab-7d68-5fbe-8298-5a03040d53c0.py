import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-18,0))
w1=cq.Workplane('ZX',origin=(0,-25,0))
r=w0.sketch().segment((-65,14),(-65,58)).arc((-69,36),(-65,14)).assemble().reset().face(w0.sketch().arc((-64,12),(16,-69),(65,34)).segment((65,12)).close().assemble()).finalize().extrude(103).union(w1.sketch().circle(100).reset().face(w1.sketch().arc((-97,27),(95,-31),(-94,38)).arc((-98,33),(-97,27)).assemble(),mode='s').finalize().extrude(70))