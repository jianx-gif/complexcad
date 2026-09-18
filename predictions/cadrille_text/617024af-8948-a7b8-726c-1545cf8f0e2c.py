import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-10,-13))
r=w0.sketch().segment((93,-10),(93,-8)).segment((95,-8)).arc((90,-10),(95,-10)).close().assemble().finalize().extrude(27)