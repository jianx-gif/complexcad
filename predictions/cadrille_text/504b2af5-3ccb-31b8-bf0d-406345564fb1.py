import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,0,-100))
r=w0.sketch().segment((25,-10),(25,10)).arc((23,0),(25,-10)).assemble().finalize().extrude(200)