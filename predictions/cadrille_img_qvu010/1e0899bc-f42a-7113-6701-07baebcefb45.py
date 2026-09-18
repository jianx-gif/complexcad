import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().circle(100).circle(99,mode='s').circle(81).finalize().extrude(200).union(w0.sketch().arc((-89,-29),(0,-85),(89,-29)).close().assemble().reset().face(w0.sketch().segment((-89,29),(89,29)).arc((0,85),(-89,29)).assemble()).finalize().extrude(200))