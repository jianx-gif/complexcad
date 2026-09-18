import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,-37,-100))
r=w0.sketch().segment((-53,19),(-53,21)).segment((-51,21)).segment((-51,18)).arc((-50,20),(-53,19)).assemble().finalize().extrude(192).union(w0.sketch().segment((28,-58),(57,-58)).segment((57,-48)).arc((42,-53),(28,-48)).close().assemble().finalize().extrude(200))