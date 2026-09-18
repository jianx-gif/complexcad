import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('ZX',origin=(0,-50,0))
r=w0.sketch().rect(80,100).circle(18,mode='s').finalize().extrude(8).union(w0.workplane(offset=13/2).cylinder(13,18)).union(w1.sketch().segment((-3,-36),(3,-36)).segment((3,-33)).arc((0,-34),(-3,-33)).close().assemble().finalize().extrude(99))
