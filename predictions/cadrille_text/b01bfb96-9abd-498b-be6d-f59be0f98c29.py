import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-55)).arc((31,-56),(29,-58)).assemble().finalize().extrude(99).union(w0.sketch().segment((29,-50),(29,-48)).segment((31,-48)).arc((10,-29),(29,-50)).assemble().finalize().extrude(100))