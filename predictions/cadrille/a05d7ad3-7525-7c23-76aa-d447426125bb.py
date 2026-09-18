import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,6))
r=w0.sketch().segment((-100,-15),(-99,-15)).arc((0,-100),(99,-15)).segment((100,-15)).segment((100,15)).segment((99,15)).arc((0,100),(-99,15)).segment((-100,15)).close().assemble().push([(-44,-67)]).circle(5,mode='s').push([(0,0)]).circle(6,mode='s').finalize().extrude(-12)