import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-10))
r=w0.sketch().segment((-100,-25),(81,-25)).segment((81,-21)).arc((100,0),(81,21)).segment((81,25)).segment((-100,25)).close().assemble().rect(188,40,mode='s').finalize().extrude(20)