import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-67))
r=w0.sketch().segment((29,-58),(36,-58)).segment((36,-42)).arc((99,0),(36,42)).segment((36,58)).segment((29,58)).segment((29,42)).arc((-24,0),(29,-42)).close().assemble().finalize().extrude(134)