import cadquery as cq
w0=cq.Workplane('YZ',origin=(-1,0,0))
w1=cq.Workplane('ZX',origin=(0,-57,0))
r=w0.sketch().circle(100).circle(89,mode='s').finalize().extrude(61).union(w1.sketch().arc((99,-19),(95,-1),(100,16)).arc((-100,1),(99,-19)).assemble().finalize().extrude(114))