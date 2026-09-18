import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-100,-100))
w1=cq.Workplane('XY',origin=(-100,-100,-100))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-55)).arc((31,-56),(29,-58)).assemble().finalize().extrude(200).union(w1.sketch().face(w1.sketch().arc((29,58),(31,56),(33,55)).segment((33,58)).close().assemble()).finalize().extrude(110))