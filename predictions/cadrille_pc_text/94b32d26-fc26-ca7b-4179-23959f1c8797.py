import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-12))
r=w0.sketch().segment((-100,-25),(-25,-25)).segment((-25,-37)).segment((25,-38)).segment((25,-25)).segment((87,-25)).arc((93,-14),(100,-4)).segment((100,25)).segment((25,25)).segment((25,37)).segment((-25,38)).segment((-25,25)).segment((-100,25)).close().assemble().finalize().extrude(25)