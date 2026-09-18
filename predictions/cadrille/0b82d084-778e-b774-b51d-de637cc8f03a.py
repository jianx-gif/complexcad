import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-8))
w1=cq.Workplane('XY',origin=(0,0,-16))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-86,-1),(-60,-1)).arc((0,-60),(60,-1)).segment((86,-1)).segment((86,1)).segment((60,1)).arc((0,60),(-60,1)).segment((-86,1)).close().assemble(),mode='s').finalize().extrude(-12).union(w1.sketch().circle(83).circle(81,mode='s').finalize().extrude(36))