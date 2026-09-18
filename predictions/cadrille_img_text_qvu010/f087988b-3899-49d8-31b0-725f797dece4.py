import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,38,0))
w1=cq.Workplane('ZX',origin=(0,1,0))
r=w0.sketch().circle(100).circle(69,mode='s').finalize().extrude(-33).union(w1.sketch().arc((-1,-1),(0,1),(1,-1)).arc((0,1),(-1,-1)).assemble().finalize().extrude(-81))