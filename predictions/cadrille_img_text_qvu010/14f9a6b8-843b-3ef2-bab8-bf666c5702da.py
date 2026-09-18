import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-54))
w1=cq.Workplane('XY',origin=(0,0,-67))
r=w0.sketch().segment((-87,96),(-86,96)).arc((-57,77),(-28,96)).segment((-27,96)).arc((-57,78),(-87,96)).assemble().finalize().extrude(-11).union(w1.sketch().arc((-86,-96),(0,-68),(86,-96)).segment((86,-96),(86,-95)).arc((0,-66),(-86,-95)).close().assemble().finalize().extrude(167))