import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,15))
r=w0.sketch().segment((-100,-37),(100,-37)).segment((100,10)).segment((-100,37)).close().assemble().push([(45,-21)]).circle(13,mode='s').finalize().extrude(-30)