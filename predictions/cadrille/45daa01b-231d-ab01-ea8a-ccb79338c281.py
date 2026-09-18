import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,34))
r=w0.sketch().circle(79).circle(34,mode='s').push([(61,-1)]).circle(8,mode='s').finalize().extrude(-68).union(w0.sketch().circle(100).circle(81,mode='s').finalize().extrude(-12))