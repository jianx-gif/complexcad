import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,4))
r=w0.sketch().segment((-100,71),(-88,-71)).segment((100,-71)).segment((100,71)).close().assemble().push([(0,35)]).circle(10,mode='s').finalize().extrude(-8)