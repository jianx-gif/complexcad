import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,30))
r=w0.sketch().push([(0,-1)]).circle(34).circle(33,mode='s').finalize().extrude(-30).union(w0.sketch().push([(0,-1)]).circle(34).circle(33,mode='s').finalize().extrude(-30))