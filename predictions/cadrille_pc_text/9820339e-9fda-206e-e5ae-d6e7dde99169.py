import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-33))
r=w0.sketch().circle(100).circle(9,mode='s').push([(87,-11)]).circle(13,mode='s').finalize().extrude(66)