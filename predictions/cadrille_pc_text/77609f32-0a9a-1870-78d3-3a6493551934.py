import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-4))
r=w0.workplane(offset=-7/2).moveTo(-22.5,0).box(95,10,7).union(w0.sketch().segment((-100,-18),(45,-18)).segment((45,-11)).segment((100,-11)).segment((100,11)).segment((45,11)).segment((45,18)).segment((-100,18)).close().assemble().push([(32,0)]).circle(10,mode='s').finalize().extrude(15))