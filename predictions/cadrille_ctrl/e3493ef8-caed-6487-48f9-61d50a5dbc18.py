import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,20))
r=w0.workplane(offset=-41/2).box(20,56,41).union(w0.sketch().rect(80,60).push([(-31,19)]).circle(2,mode='s').push([(-29,-19)]).circle(1,mode='s').push([(28,-19)]).circle(2,mode='s').push([(29,18)]).circle(2,mode='s').finalize().extrude(-20))
