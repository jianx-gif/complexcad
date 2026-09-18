import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,99,0))
w1=cq.Workplane('ZX',origin=(0,35,0))
r=w0.sketch().segment((-60,-1),(-33,35)).arc((-50,20),(-60,-1)).assemble().reset().face(w0.sketch().arc((-15,-59),(15,-44),(33,-15)).segment((60,-35)).segment((60,1)).segment((33,-35)).arc((15,-44),(-6,-59)).close().assemble()).finalize().extrude(-198).union(w1.sketch().circle(100).circle(99,mode='s').finalize().extrude(-55))