import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,-57,-1))
w1=cq.Workplane('XY',origin=(-57,-57,-33))
r=w0.sketch().segment((-53,18),(-49,18)).segment((-49,22)).close().assemble().finalize().extrude(10).union(w1.sketch().segment((28,-58),(28,-57)).segment((30,-57)).arc((34,-56),(37,-57)).segment((39,-57)).arc((34,-48),(28,-58)).assemble().finalize().extrude(-33))