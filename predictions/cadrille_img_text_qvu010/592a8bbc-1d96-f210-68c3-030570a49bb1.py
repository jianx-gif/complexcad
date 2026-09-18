import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-17,0))
w1=cq.Workplane('ZX',origin=(0,-78,0))
r=w0.sketch().circle(100).circle(97,mode='s').finalize().extrude(43).union(w1.sketch().arc((-3,-1),(0,-3),(3,-1)).close().assemble().finalize().extrude(156))