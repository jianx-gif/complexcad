import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,11))
r=w0.sketch().circle(100).circle(45,mode='s').push([(1,-85)]).circle(2,mode='s').finalize().extrude(-22)