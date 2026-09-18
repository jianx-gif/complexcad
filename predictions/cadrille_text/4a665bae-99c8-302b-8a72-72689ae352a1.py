import cadquery as cq
w0=cq.Workplane('XY',origin=(-50,-100,-50))
r=w0.sketch().segment((-47,100),(-46,97)).segment((-46,100)).close().assemble().reset().face(w0.sketch().segment((46,-100),(47,-100)).segment((46,-97)).close().assemble()).finalize().extrude(100)