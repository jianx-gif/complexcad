import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().circle(23).reset().face(w0.sketch().segment((-20,-5),(-16,-5)).arc((0,-17),(16,-5)).segment((20,-5)).segment((20,5)).segment((16,5)).arc((0,17),(-16,5)).segment((-20,5)).close().assemble(),mode='s').finalize().extrude(-200).union(w0.sketch().circle(29).circle(26,mode='s').finalize().extrude(-5))