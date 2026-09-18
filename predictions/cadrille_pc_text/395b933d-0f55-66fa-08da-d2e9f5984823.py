import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-44))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().circle(100).circle(92,mode='s').finalize().extrude(100).union(w1.sketch().segment((-57,-100),(-30,-100)).segment((-30,-90)).arc((-44,-91),(-57,-90)).close().assemble().finalize().extrude(200))