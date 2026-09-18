import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,34,0))
w1=cq.Workplane('ZX',origin=(0,77,0))
r=w0.sketch().circle(100).circle(94,mode='s').finalize().extrude(-67).union(w1.sketch().segment((-34,-53),(34,-53)).segment((34,-38)).arc((0,-49),(-34,-38)).close().assemble().finalize().extrude(-155))