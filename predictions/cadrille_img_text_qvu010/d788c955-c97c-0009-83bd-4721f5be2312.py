import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-70,0))
r=w0.sketch().circle(100).reset().face(w0.sketch().arc((-87,-48),(87,50),(-82,-56)).segment((-81,-56)).arc((86,50),(-87,-48)).assemble(),mode='s').finalize().extrude(23).union(w0.sketch().arc((-27,-25),(11,-19),(27,16)).segment((-1,29)).arc((-13,24),(-24,18)).arc((-22,-4),(-27,-25)).assemble().finalize().extrude(141))