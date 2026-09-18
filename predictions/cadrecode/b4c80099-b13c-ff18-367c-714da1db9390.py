import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,6))
w1=cq.Workplane('XY',origin=(0,0,28))
r=w0.sketch().circle(97).reset().face(w0.sketch().segment((-93,-10),(-64,-10)).arc((-1,-70),(64,-10)).segment((93,-10)).segment((93,10)).segment((64,10)).arc((-1,70),(-64,10)).segment((-93,10)).close().assemble(),mode='s').finalize().extrude(-34).union(w0.workplane(offset=11/2).cylinder(11,100)).union(w1.sketch().arc((-87,-49),(0,65),(87,-49)).segment((87,49)).segment((64,49)).arc((0,96),(-64,49)).segment((-87,49)).close().assemble().finalize().extrude(-11))