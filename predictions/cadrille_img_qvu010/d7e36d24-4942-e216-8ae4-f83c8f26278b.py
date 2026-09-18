import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-42,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().circle(100).circle(79,mode='s').circle(58).circle(43,mode='s').circle(28).finalize().extrude(119).union(w1.sketch().circle(58).reset().face(w1.sketch().segment((-24,-18),(-18,-18)).arc((0,-25),(18,-18)).segment((24,-18)).segment((24,-13)).arc((25,-8),(24,-3)).segment((24,18)).segment((18,18)).arc((0,25),(-18,18)).segment((-24,18)).close().assemble(),mode='s').finalize().extrude(199))