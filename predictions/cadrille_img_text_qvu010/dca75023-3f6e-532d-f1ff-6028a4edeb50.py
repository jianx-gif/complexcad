import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,91,0))
w1=cq.Workplane('ZX',origin=(0,48,0))
r=w0.sketch().segment((-74,-70),(74,-70)).segment((74,-39)).arc((0,-73),(-74,-39)).close().assemble().finalize().extrude(-162).union(w0.sketch().segment((-74,-31),(74,-31)).segment((74,31)).segment((-74,31)).segment((-74,29)).arc((-70,27),(-74,25)).close().assemble().finalize().extrude(-159)).union(w1.sketch().arc((-100,-22),(-77,33),(-100,87)).close().assemble().finalize().extrude(-96))