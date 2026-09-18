import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('XY',origin=(0,0,-66))
r=w0.sketch().segment((-99,-19),(-78,-19)).arc((-92,0),(-99,19)).close().assemble().reset().face(w0.sketch().segment((-76,-19),(76,-19)).segment((76,19)).arc((0,-92),(-76,19)).close().assemble()).reset().face(w0.sketch().arc((-76,19),(0,92),(76,19)).segment((76,17)).arc((77,0),(76,-17)).close().assemble()).finalize().extrude(200).union(w1.sketch().arc((-11,-95),(11,-77),(25,-53)).arc((10,-76),(-11,-95)).assemble().finalize().extrude(119))