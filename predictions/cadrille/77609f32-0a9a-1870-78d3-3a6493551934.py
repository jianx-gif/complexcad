import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-4))
w1=cq.Workplane('YZ',origin=(15,0,0))
r=w0.sketch().segment((-100,-18),(45,-18)).segment((45,-11)).segment((100,-11)).segment((100,11)).segment((45,11)).segment((45,18)).segment((-100,18)).close().assemble().push([(33,0)]).circle(2,mode='s').push([(50,0)]).circle(11,mode='s').finalize().extrude(15).union(w1.workplane(offset=-115/2).moveTo(0,-3.5).box(10,15,115))