import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-58,0))
w1=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().circle(100).circle(93,mode='s').finalize().extrude(150).union(w1.sketch().arc((33,-92),(84,-50),(98,14)).segment((33,14)).close().assemble().finalize().extrude(20))