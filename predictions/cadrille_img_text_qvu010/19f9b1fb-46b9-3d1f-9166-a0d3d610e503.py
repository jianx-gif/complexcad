import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-38,0))
w1=cq.Workplane('ZX',origin=(0,-1,0))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-97,46),(-88,37)).arc((-66,-57),(30,-75)).segment((39,-84)).segment((97,-46)).segment((88,-37)).arc((66,57),(-30,75)).segment((-39,84)).close().assemble(),mode='s').circle(62).finalize().extrude(33).union(w1.sketch().arc((57,-82),(100,-18),(57,46)).close().assemble().finalize().extrude(-37))