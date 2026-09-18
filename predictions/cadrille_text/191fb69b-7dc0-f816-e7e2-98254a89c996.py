import cadquery as cq
w0=cq.Workplane('XY',origin=(-60,-100,-36))
r=w0.sketch().segment((-60,96),(-59,96)).segment((-59,97)).close().assemble().reset().face(w0.sketch().segment((59,-97),(60,-96)).segment((59,-96)).close().assemble()).finalize().extrude(72).union(w0.workplane(offset=72/2).cylinder(72,36))