import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-60,-60))
r=w0.sketch().segment((-100,60),(-99,57)).segment((-99,60)).close().assemble().reset().face(w0.sketch().segment((99,-60),(100,-60)).segment((99,-57)).close().assemble()).finalize().extrude(120)