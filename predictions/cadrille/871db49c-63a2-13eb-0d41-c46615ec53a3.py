import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().circle(18).reset().face(w0.sketch().segment((-20,-4),(-16,-4)).arc((0,-13),(16,-4)).segment((20,-4)).segment((20,4)).segment((16,4)).arc((0,13),(-16,4)).segment((-20,4)).close().assemble(),mode='s').finalize().extrude(-200).union(w0.sketch().circle(29).circle(27,mode='s').finalize().extrude(-106))