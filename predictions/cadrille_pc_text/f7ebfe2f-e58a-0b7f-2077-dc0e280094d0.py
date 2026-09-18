import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-12))
r=w0.sketch().segment((-100,-62),(-88,-62)).segment((-88,-75)).segment((88,-75)).segment((88,-62)).segment((100,-62)).segment((100,62)).segment((88,62)).segment((88,75)).segment((-11,75)).arc((-50,4),(-99,-57)).close().assemble().finalize().extrude(25)