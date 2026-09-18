import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-25,0))
w1=cq.Workplane('ZX',origin=(0,-86,0))
r=w0.sketch().circle(100).circle(95,mode='s').finalize().extrude(51).union(w1.sketch().arc((-3,-1),(0,-3),(3,-1)).close().assemble().finalize().extrude(172))