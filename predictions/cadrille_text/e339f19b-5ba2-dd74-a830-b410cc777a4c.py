import cadquery as cq
w0=cq.Workplane('XY',origin=(-50,-100,-100))
r=w0.sketch().segment((-48,96),(-47,96)).segment((-47,98)).close().assemble().reset().face(w0.sketch().segment((47,-8),(48,-9)).segment((48,-96)).segment((47,-96)).close().assemble()).finalize().extrude(200)