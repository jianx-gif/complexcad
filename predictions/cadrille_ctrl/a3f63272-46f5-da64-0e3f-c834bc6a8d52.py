import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,11))
r=w0.sketch().circle(45).reset().face(w0.sketch().segment((-39,-14),(-36,-14)).arc((0,-38),(36,-14)).segment((39,-14)).segment((39,14)).segment((36,14)).arc((0,38),(-36,14)).segment((-39,14)).close().assemble(),mode='s').finalize().extrude(-11).union(w0.sketch().circle(45).circle(27,mode='s').finalize().extrude(-9))
