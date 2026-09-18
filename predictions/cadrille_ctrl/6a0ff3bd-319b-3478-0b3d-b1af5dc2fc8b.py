import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((-25,-14),(23,-15)).segment((25,14)).segment((-23,15)).close().assemble().circle(12,mode='s').finalize().extrude(31).union(w0.sketch().segment((-25,-1),(-16,-1)).arc((-1,-13),(16,-10)).segment((16,-6)).segment((18,-6)).arc((19,0),(18,6)).segment((18,11)).segment((16,11)).arc((0,11),(-13,2)).segment((-13,11)).segment((-16,11)).segment((-16,6)).arc((-18,4),(-19,1)).segment((-25,1)).close().assemble().circle(11,mode='s').finalize().extrude(80)).union(w0.workplane(offset=100/2).cylinder(100,13))
