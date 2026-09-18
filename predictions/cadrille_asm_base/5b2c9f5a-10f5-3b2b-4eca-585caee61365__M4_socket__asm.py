import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,6))
w1=cq.Workplane('XY',origin=(0,0,28))
r=w0.sketch().segment((-100,-75),(-12,-75)).arc((0,-76),(12,-75)).segment((100,-75)).segment((100,75)).segment((12,75)).arc((0,76),(-12,75)).segment((-100,75)).close().assemble().push([(71,-57)]).circle(2,mode='s').finalize().extrude(-13).union(w1.sketch().circle(17).rect(24,18,mode='s').finalize().extrude(-55))