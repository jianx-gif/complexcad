import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,0,-100))
r=w0.sketch().segment((-53,15),(-48,15)).arc((-51,17),(-53,19)).close().assemble().reset().face(w0.sketch().segment((48,-15),(53,-15)).segment((53,-19)).arc((51,-17),(48,-15)).assemble()).finalize().extrude(199).union(w0.workplane(offset=200/2).cylinder(200,3))