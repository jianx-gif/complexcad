import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('ZX',origin=(0,74,0))
r=w0.sketch().segment((-50,-50),(32,-50)).arc((-41,45),(50,-33)).segment((50,50)).segment((-50,50)).close().assemble().finalize().extrude(-200).union(w1.sketch().circle(100).circle(67,mode='s').finalize().extrude(-168))