import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-23,0))
w1=cq.Workplane('ZX',origin=(0,77,0))
r=w0.sketch().circle(100).circle(35,mode='s').circle(25).finalize().extrude(18).union(w1.sketch().arc((-1,-1),(0,0),(1,-1)).segment((1,1)).segment((-1,1)).close().assemble().finalize().extrude(-155))