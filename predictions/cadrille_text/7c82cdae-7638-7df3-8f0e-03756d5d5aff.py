import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,0,-100))
r=w0.sketch().segment((-53,18),(-47,18)).segment((-53,21)).close().assemble().reset().face(w0.sketch().segment((47,-18),(53,-21)).segment((53,-18)).close().assemble()).finalize().extrude(200)