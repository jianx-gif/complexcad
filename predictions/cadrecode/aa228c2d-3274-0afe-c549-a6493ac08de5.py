import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().segment((-88,-100),(88,-100)).segment((88,-75)).segment((-62,-75)).segment((-62,87)).segment((-13,88)).segment((-12,88)).segment((-12,100)).segment((-88,100)).close().assemble().finalize().extrude(-20)