import cadquery as cq
w0=cq.Workplane('YZ',origin=(68,0,0))
r=w0.sketch().rect(200,154).reset().face(w0.sketch().segment((-73,-23),(-34,-23)).arc((0,-41),(34,-23)).segment((73,-23)).segment((73,23)).segment((34,23)).arc((0,41),(-34,23)).segment((-73,23)).close().assemble(),mode='s').finalize().extrude(-136)