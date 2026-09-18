import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,89,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-77,-4),(-71,-25)).segment((77,4)).segment((71,25)).close().assemble().finalize().extrude(-139).union(w1.sketch().segment((-89,-11),(-35,-11)).arc((0,-35),(35,-11)).segment((89,-11)).segment((89,11)).segment((35,11)).arc((0,35),(-35,11)).segment((-89,11)).close().assemble().finalize().extrude(-200))