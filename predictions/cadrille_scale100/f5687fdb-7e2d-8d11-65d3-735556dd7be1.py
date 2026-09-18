import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,10,0))
w1=cq.Workplane('ZX',origin=(0,13,0))
r=w0.sketch().segment((-30,-10),(-18,-10)).arc((0,-21),(18,-10)).segment((30,-10)).segment((30,10)).segment((18,10)).arc((0,21),(-18,10)).segment((-30,10)).close().assemble().circle(14,mode='s').finalize().extrude(-20).union(w0.sketch().segment((-15,0),(-1,-15)).segment((15,0)).segment((1,15)).close().assemble().finalize().extrude(17)).union(w1.sketch().circle(25).circle(14,mode='s').finalize().extrude(-28))