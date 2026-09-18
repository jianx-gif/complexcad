import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-12))
w1=cq.Workplane('XY',origin=(-78,-11,-12))
r=w0.sketch().segment((-100,85),(-12,-28)).segment((30,5)).segment((-88,100)).close().assemble().finalize().extrude(24).union(w1.sketch().segment((-78,-100),(8,-100)).segment((8,-97)).segment((100,-97)).segment((100,-100)).segment((100,-11)).segment((-78,-11)).close().assemble().finalize().extrude(-10))