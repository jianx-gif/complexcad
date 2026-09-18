import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-13))
r=w0.sketch().segment((-100,50),(-79,10)).arc((1,15),(56,-55)).segment((55,-67)).segment((100,-67)).arc((44,42),(-100,50)).assemble().finalize().extrude(26)