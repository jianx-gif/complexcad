import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-100,-100))
w1=cq.Workplane('XY',origin=(-100,-100,-100))
r=w0.sketch().circle(40).circle(32,mode='s').finalize().extrude(200).union(w1.sketch().face(w1.sketch().segment((29,-58),(33,-58)).arc((31,-57),(29,-58)).assemble()).finalize().extrude(110))