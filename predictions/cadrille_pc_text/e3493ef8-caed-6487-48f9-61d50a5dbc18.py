import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,51))
r=w0.sketch().rect(50,140).push([(10,-48)]).circle(5,mode='s').finalize().extrude(-102).union(w0.sketch().segment((-100,-75),(100,-75)).segment((100,75)).segment((-100,75)).segment((-100,67)).segment((-73,67)).segment((-73,42)).segment((-100,42)).close().assemble().push([(83,-44)]).circle(16,mode='s').finalize().extrude(-50))