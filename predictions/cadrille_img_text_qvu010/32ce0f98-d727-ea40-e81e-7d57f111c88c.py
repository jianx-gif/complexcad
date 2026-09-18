import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-74,-77),(14,-25),(79,48)).arc((10,-17),(-74,-77)).assemble().finalize().extrude(19).union(w0.sketch().segment((-60,-57),(-59,-57)).arc((-29,-21),(15,-5)).segment((15,-4)).arc((44,28),(60,69)).segment((60,70)).segment((59,70)).arc((29,77),(-4,70)).segment((-59,-57)).close().assemble().finalize().extrude(200))