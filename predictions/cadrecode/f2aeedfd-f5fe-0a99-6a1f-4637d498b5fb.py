import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-10))
r=w0.sketch().segment((-100,-25),(98,-25)).arc((100,-2),(99,22)).segment((99,25)).segment((-57,25)).segment((-57,16)).segment((-66,16)).segment((-66,25)).segment((-100,25)).close().assemble().finalize().extrude(20)