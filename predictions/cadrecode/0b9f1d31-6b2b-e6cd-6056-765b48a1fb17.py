import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-77,33),(-10,-83)).segment((77,-33)).segment((10,83)).close().assemble().finalize().extrude(200).union(w0.sketch().segment((-76,33),(-10,-83)).segment((76,-33)).segment((10,83)).close().assemble().finalize().extrude(200))