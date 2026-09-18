import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('XY',origin=(0,0,2))
r=w0.sketch().segment((-15,-15),(-10,-15)).arc((0,-20),(10,-15)).segment((15,-15)).segment((15,-10)).arc((22,1),(15,13)).segment((15,18)).segment((10,18)).arc((0,22),(-10,18)).segment((-15,18)).segment((-15,13)).arc((-22,1),(-15,-10)).close().assemble().finalize().extrude(-4).union(w0.sketch().push([(0,1)]).circle(14).circle(13,mode='s').finalize().extrude(2)).union(w1.sketch().push([(-2,0)]).circle(15).circle(13,mode='s').finalize().extrude(58))