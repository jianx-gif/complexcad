import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
r=w0.sketch().segment((-100,-75),(100,-75)).segment((100,-50)).segment((-75,-50)).segment((-75,75)).segment((-100,75)).close().assemble().reset().face(w0.sketch().segment((-58,-70),(-43,-70)).segment((-42,-57)).segment((-57,-55)).close().assemble(),mode='s').push([(50,-62)]).circle(8,mode='s').finalize().extrude(-24)