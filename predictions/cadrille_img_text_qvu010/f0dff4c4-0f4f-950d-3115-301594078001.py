import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-30,0))
w1=cq.Workplane('XY',origin=(0,0,-3))
r=w0.sketch().circle(100).circle(93,mode='s').circle(61).finalize().extrude(95).union(w1.sketch().arc((-79,-20),(-45,-21),(-18,-41)).segment((18,-41)).segment((18,41)).segment((-18,41)).segment((-18,20)).arc((-52,21),(-79,0)).close().assemble().finalize().extrude(-89))