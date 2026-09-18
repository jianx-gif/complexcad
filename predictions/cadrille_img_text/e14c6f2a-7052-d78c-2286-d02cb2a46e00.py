import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,97,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((-45,-36),(0,-56),(45,-36)).close().assemble().reset().face(w0.sketch().segment((-45,36),(45,36)).arc((0,56),(-45,36)).assemble()).finalize().extrude(-195).union(w1.sketch().circle(88).circle(79,mode='s').finalize().extrude(-187))