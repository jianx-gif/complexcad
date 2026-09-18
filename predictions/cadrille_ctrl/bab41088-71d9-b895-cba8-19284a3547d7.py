import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('XY',origin=(0,0,34))
r=w0.sketch().segment((-25,-2),(21,-4)).segment((22,11)).arc((18,19),(16,28)).segment((-15,29)).arc((-17,27),(-19,29)).segment((-19,28)).arc((-21,21),(-20,14)).segment((-23,14)).close().assemble().finalize().extrude(24).union(w0.sketch().segment((-21,-6),(-19,-6)).arc((-1,-18),(17,-8)).segment((19,-8)).segment((21,11)).segment((19,11)).arc((1,23),(-17,13)).segment((-19,13)).close().assemble().finalize().extrude(80)).union(w1.sketch().arc((15,40),(16,39),(17,39)).segment((17,40)).close().assemble().finalize().extrude(-134))
