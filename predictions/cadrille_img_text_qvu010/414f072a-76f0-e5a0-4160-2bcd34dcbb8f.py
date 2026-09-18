import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().circle(100).circle(58,mode='s').finalize().extrude(-200).union(w0.sketch().arc((-96,-32),(0,-96),(96,-32)).close().assemble().reset().face(w0.sketch().segment((-96,32),(96,32)).arc((0,96),(-96,32)).assemble()).finalize().extrude(-135))