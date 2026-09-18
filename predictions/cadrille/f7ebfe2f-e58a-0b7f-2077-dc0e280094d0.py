import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
r=w0.sketch().segment((-100,-63),(-88,-63)).segment((-88,-75)).segment((88,-75)).segment((88,-63)).segment((100,-63)).segment((100,63)).segment((88,63)).segment((88,75)).segment((-11,75)).segment((-35,4)).segment((-94,6)).segment((-94,-15)).segment((-100,-15)).close().assemble().finalize().extrude(-24)