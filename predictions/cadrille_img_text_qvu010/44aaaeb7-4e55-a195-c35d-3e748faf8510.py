import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-7,-75),(2,-73),(10,-70)).segment((75,-70)).segment((75,-6)).segment((10,-6)).arc((2,-2),(-7,0)).close().assemble().finalize().extrude(-200).union(w0.sketch().segment((-75,-11),(-66,-11)).arc((-32,58),(32,75)).arc((-24,68),(-66,26)).segment((-75,26)).close().assemble().finalize().extrude(-183))