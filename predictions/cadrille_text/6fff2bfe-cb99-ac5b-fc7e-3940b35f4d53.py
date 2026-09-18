import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,-100,-100))
r=w0.sketch().segment((-57,100),(-56,97)).segment((-56,100)).close().assemble().reset().face(w0.sketch().segment((56,-100),(57,-100)).segment((56,-97)).close().assemble()).finalize().extrude(200)