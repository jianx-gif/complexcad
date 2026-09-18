import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,89))
w1=cq.Workplane('ZX',origin=(0,-14,0))
r=w0.sketch().segment((-93,-15),(93,-12)).segment((93,15)).segment((-93,12)).close().assemble().circle(7,mode='s').finalize().extrude(-163).union(w1.sketch().circle(100).circle(81,mode='s').finalize().extrude(28))