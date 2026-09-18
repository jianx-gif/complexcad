import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('XY',origin=(0,0,-83))
r=w0.sketch().segment((-75,21),(-74,21)).arc((-44,-45),(19,-75)).segment((-55,48)).segment((13,96)).arc((-37,78),(-74,33)).segment((-75,33)).close().assemble().reset().face(w0.sketch().arc((19,-75),(62,-45),(75,6)).segment((74,6)).arc((62,52),(19,81)).segment((19,21)).segment((55,-48)).segment((19,-67)).close().assemble()).finalize().extrude(200).union(w1.sketch().arc((-13,-96),(1,-90),(13,-81)).arc((-1,-89),(-13,-96)).assemble().finalize().extrude(-17))