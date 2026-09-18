import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-29,0))
w1=cq.Workplane('ZX',origin=(0,-38,0))
r=w0.sketch().circle(100).circle(85,mode='s').finalize().extrude(43).union(w1.sketch().arc((-1,-1),(1,0),(3,0)).arc((-1,1),(-1,-1)).assemble().finalize().extrude(-52))