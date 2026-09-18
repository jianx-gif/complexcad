import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-100,-100))
w1=cq.Workplane('XY',origin=(-100,-100,-100))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-57)).close().assemble().finalize().extrude(200).union(w1.workplane(offset=110/2).moveTo(0,10).cylinder(110,2))