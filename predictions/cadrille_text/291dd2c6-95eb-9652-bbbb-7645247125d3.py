import cadquery as cq
w0=cq.Workplane('XY',origin=(-77,0,-100))
r=w0.sketch().segment((-71,39),(-69,39)).segment((-69,41)).close().assemble().reset().face(w0.sketch().segment((69,-41),(71,-39)).segment((69,-39)).close().assemble()).finalize().extrude(200)