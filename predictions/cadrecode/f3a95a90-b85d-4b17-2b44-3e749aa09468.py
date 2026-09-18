import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,1))
r=w0.workplane(offset=-15/2).box(200,76,15).union(w0.sketch().segment((-38,-18),(37,-18)).segment((38,18)).segment((-36,19)).close().assemble().push([(-24,5)]).circle(3,mode='s').push([(24,-4)]).circle(3,mode='s').finalize().extrude(13))