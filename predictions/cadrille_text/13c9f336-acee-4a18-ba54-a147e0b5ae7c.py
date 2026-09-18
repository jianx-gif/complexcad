import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-100,-100))
w1=cq.Workplane('XY',origin=(-100,-100,-100))
r=w0.sketch().segment((-100,-100),(-99,-100)).segment((-100,-97)).close().assemble().finalize().extrude(200).union(w1.workplane(offset=110/2).moveTo(0,-10).box(10,10,110))