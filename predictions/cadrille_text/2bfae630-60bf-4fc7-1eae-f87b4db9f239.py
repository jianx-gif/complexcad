import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-57))
w1=cq.Workplane('XY',origin=(0,0,-26))
r=w0.sketch().face(w0.sketch().segment((0,0),(3,-3)).segment((3,0)).close().assemble()).finalize().extrude(114).union(w1.sketch().face(w1.sketch().segment((0,0),(3,0)).segment((3,3)).arc((1,2),(0,3)).close().assemble()).finalize().extrude(-74))