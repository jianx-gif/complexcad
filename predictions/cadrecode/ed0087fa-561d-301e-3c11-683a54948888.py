import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,34))
w1=cq.Workplane('XY',origin=(0,0,33))
r=w0.sketch().circle(83).reset().face(w0.sketch().segment((-86,-10),(-49,-10)).arc((0,-46),(49,-10)).segment((86,-10)).segment((86,10)).segment((49,10)).arc((0,46),(-49,10)).segment((-86,10)).close().assemble(),mode='s').finalize().extrude(-67).union(w0.workplane(offset=-48/2).cylinder(48,100)).union(w1.sketch().circle(97).circle(34,mode='s').finalize().extrude(-61))