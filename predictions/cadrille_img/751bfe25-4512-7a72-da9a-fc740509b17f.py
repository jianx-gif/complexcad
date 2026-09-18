import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,1,0))
w1=cq.Workplane('ZX',origin=(0,-13,0))
r=w0.sketch().circle(100).reset().face(w0.sketch().arc((-70,33),(67,-50),(-17,81)).arc((-49,63),(-70,33)).assemble(),mode='s').push([(28,46)]).circle(31).finalize().extrude(-16).union(w1.sketch().arc((-10,84),(6,-85),(10,84)).arc((0,81),(-10,84)).assemble().finalize().extrude(35))