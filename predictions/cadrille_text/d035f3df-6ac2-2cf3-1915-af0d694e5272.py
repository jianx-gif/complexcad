import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('XY',origin=(0,0,-62))
r=w0.sketch().face(w0.sketch().segment((0,0),(3,-3)).segment((3,0)).close().assemble()).finalize().extrude(200).union(w1.sketch().face(w1.sketch().segment((33,2),(33,3)).arc((31,0),(35,2)).close().assemble()).finalize().extrude(129))