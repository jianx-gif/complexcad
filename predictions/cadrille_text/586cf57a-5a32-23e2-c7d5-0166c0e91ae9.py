import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-60,-60))
r=w0.sketch().face(w0.sketch().segment((91,-43),(100,60)).arc((96,57),(91,55)).close().assemble()).finalize().extrude(120)