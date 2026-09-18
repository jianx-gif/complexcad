import cadquery as cq
w0=cq.Workplane('XY',origin=(-33,-27,-100))
r=w0.sketch().segment((27,-58),(33,-58)).segment((33,-27)).arc((30,-29),(27,-27)).close().assemble().finalize().extrude(200)