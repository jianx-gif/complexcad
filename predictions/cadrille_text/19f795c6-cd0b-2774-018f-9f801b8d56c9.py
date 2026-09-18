import cadquery as cq
w0=cq.Workplane('XY',origin=(-67,0,-100))
r=w0.sketch().segment((27,-58),(33,-58)).segment((33,-52)).arc((30,-55),(27,-58)).assemble().finalize().extrude(200)