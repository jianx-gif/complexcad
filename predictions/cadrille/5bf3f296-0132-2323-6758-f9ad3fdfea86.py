import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,69))
w1=cq.Workplane('XY',origin=(0,0,56))
r=w0.sketch().segment((-100,46),(-93,-51)).segment((100,-49)).segment((93,51)).close().assemble().reset().face(w0.sketch().segment((-84,1),(-74,-14)).segment((-51,-1)).segment((-61,14)).close().assemble(),mode='s').push([(0,0)]).circle(35,mode='s').push([(69,-1)]).circle(14,mode='s').finalize().extrude(-59).union(w1.sketch().segment((-77,10),(-56,10)).segment((-56,-13)).segment((-76,-13)).arc((77,10),(-77,10)).assemble().push([(1,0)]).circle(35,mode='s').finalize().extrude(-125))