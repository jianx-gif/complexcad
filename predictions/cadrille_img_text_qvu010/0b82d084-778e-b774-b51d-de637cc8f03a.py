import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,39,0))
w1=cq.Workplane('ZX',origin=(0,75,0))
r=w0.sketch().circle(99).circle(77,mode='s').finalize().extrude(-32).union(w1.sketch().arc((-1,-1),(0,1),(1,-1)).segment((1,1)).segment((-1,1)).close().assemble().finalize().extrude(-150))