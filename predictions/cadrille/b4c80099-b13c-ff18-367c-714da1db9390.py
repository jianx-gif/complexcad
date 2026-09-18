import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,6))
w1=cq.Workplane('XY',origin=(0,0,28))
r=w0.sketch().circle(98).reset().face(w0.sketch().segment((-87,11),(-64,-14)).arc((-49,-45),(-20,-64)).segment((3,-89)).segment((87,-11)).segment((64,14)).arc((49,45),(20,64)).segment((-3,89)).close().assemble(),mode='s').finalize().extrude(-32).union(w0.workplane(offset=11/2).cylinder(11,100)).union(w1.sketch().circle(93).circle(72,mode='s').finalize().extrude(-11))