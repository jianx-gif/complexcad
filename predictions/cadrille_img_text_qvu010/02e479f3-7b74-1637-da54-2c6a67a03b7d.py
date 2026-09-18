import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,10,0))
w1=cq.Workplane('ZX',origin=(0,29,0))
r=w0.sketch().circle(86).circle(67,mode='s').finalize().extrude(-49).union(w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(69)).union(w1.sketch().arc((-34,-53),(0,-60),(34,-53)).close().assemble().finalize().extrude(-119))