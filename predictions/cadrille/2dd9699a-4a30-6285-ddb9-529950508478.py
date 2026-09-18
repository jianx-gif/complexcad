import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,2))
r=w0.sketch().rect(194,200).push([(-73,-75)]).circle(5,mode='s').push([(0,14)]).circle(6,mode='s').push([(73,-75)]).circle(3,mode='s').push([(74,14)]).circle(2,mode='s').finalize().extrude(-19).union(w0.workplane(offset=15/2).box(14,200,15))