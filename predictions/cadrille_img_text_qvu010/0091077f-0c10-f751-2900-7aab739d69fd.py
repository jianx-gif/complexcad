import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-80,11),(-26,75)).arc((-57,49),(-80,11)).assemble().reset().face(w0.sketch().arc((-26,-75),(-16,-70),(-7,-63)).close().assemble()).reset().face(w0.sketch().segment((7,63),(26,49)).arc((18,58),(7,63)).assemble()).finalize().extrude(-200)