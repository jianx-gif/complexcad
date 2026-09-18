import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-28,0))
w1=cq.Workplane('ZX',origin=(0,-10,0))
r=w0.sketch().circle(82).circle(30,mode='s').finalize().extrude(-32).union(w0.sketch().segment((-67,-75),(67,-75)).segment((67,75)).segment((55,75)).arc((53,71),(51,75)).segment((-67,75)).close().assemble().finalize().extrude(120)).union(w1.sketch().rect(200,198).circle(97,mode='s').finalize().extrude(28))