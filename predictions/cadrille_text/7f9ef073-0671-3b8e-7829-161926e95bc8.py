import cadquery as cq
w0=cq.Workplane('XY',origin=(-60,-100,-80))
r=w0.sketch().segment((-60,96),(-59,96)).segment((-59,98)).close().assemble().reset().face(w0.sketch().segment((59,-98),(60,-96)).segment((59,-96)).close().assemble()).finalize().extrude(160).union(w0.sketch().circle(30).circle(26,mode='s').finalize().extrude(160))