import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-45,0))
w1=cq.Workplane('ZX',origin=(0,-97,0))
r=w0.sketch().circle(100).circle(97,mode='s').finalize().extrude(-5).union(w0.sketch().arc((-34,-63),(0,-71),(34,-63)).close().assemble().finalize().extrude(132)).union(w1.sketch().circle(71).circle(14,mode='s').finalize().extrude(194))