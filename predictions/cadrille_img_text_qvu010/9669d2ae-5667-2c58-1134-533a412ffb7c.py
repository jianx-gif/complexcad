import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-45,0))
r=w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(-5).union(w0.sketch().arc((-29,-61),(0,-67),(29,-61)).close().assemble().reset().face(w0.sketch().segment((-29,61),(29,61)).arc((0,67),(-29,61)).assemble()).finalize().extrude(135))