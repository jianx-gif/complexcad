import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,22))
w1=cq.Workplane('XY',origin=(0,0,3))
r=w0.sketch().segment((-88,-11),(-65,-11)).segment((-88,11)).close().assemble().reset().face(w0.sketch().segment((-88,11),(-64,11)).segment((-64,13)).segment((-88,13)).close().assemble()).reset().face(w0.sketch().segment((-64,-11),(-40,-33)).segment((-40,-11)).close().assemble()).reset().face(w0.sketch().segment((12,33),(33,11)).segment((33,13)).segment((14,13)).close().assemble()).finalize().extrude(-44).union(w1.sketch().rect(200,120).rect(34,78,mode='s').finalize().extrude(-8))