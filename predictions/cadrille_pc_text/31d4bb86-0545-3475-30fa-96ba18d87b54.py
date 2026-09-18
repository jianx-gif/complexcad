import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-37))
r=w0.sketch().segment((-100,-50),(100,-50)).segment((100,50)).segment((-100,50)).segment((-100,42)).arc((-94,26),(-100,10)).close().assemble().push([(-62,25)]).circle(6,mode='s').push([(44,46)]).circle(6,mode='s').finalize().extrude(75)