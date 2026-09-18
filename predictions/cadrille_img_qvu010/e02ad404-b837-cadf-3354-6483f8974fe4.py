import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,1,0))
w1=cq.Workplane('ZX',origin=(0,38,0))
r=w0.sketch().circle(100).circle(74,mode='s').finalize().extrude(-18).union(w1.sketch().circle(99).reset().face(w1.sketch().segment((-22,-75),(22,-75)).segment((22,-67)).arc((70,0),(22,67)).segment((22,75)).segment((-22,75)).segment((-22,67)).arc((-70,0),(-22,-67)).close().assemble(),mode='s').finalize().extrude(33))