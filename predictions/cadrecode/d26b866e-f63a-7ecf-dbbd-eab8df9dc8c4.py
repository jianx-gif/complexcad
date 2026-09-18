import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,22))
r=w0.sketch().rect(176,76).push([(39,-36)]).circle(3,mode='s').push([(42,36)]).circle(2,mode='s').finalize().extrude(-45).union(w0.sketch().circle(100).push([(39,36)]).circle(7,mode='s').finalize().extrude(-24))