import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,6))
r=w0.sketch().segment((-100,-75),(100,-75)).segment((100,75)).segment((-100,75)).segment((-100,57)).segment((-98,57)).segment((-98,54)).segment((-100,54)).close().assemble().push([(-62,-11)]).circle(7,mode='s').finalize().extrude(-12)