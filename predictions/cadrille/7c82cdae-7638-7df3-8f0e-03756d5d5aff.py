import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,2))
r=w0.sketch().segment((-100,-75),(100,-75)).segment((100,-25)).segment((-50,-25)).segment((-50,75)).segment((-100,75)).close().assemble().finalize().extrude(-4)