import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-24,0))
w1=cq.Workplane('XY',origin=(0,0,-39))
r=w0.sketch().circle(100).circle(85,mode='s').finalize().extrude(21).union(w1.sketch().arc((-1,76),(-1,-76),(1,76)).segment((1,79)).segment((-1,79)).close().assemble().reset().face(w1.sketch().segment((-1,-34),(-1,-1)).arc((-10,-18),(-1,-34)).assemble(),mode='s').reset().face(w1.sketch().arc((1,-34),(10,-18),(1,-1)).close().assemble(),mode='s').finalize().extrude(43))