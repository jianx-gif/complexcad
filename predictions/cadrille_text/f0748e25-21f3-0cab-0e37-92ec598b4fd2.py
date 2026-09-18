import cadquery as cq
w0=cq.Workplane('XY',origin=(-50,-50,-100))
r=w0.sketch().segment((-50,100),(-46,93)).segment((-46,100)).close().assemble().reset().face(w0.sketch().segment((46,-100),(50,-100)).segment((46,-93)).close().assemble()).finalize().extrude(200)