import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-57,0))
w1=cq.Workplane('ZX',origin=(0,-25,0))
r=w0.sketch().segment((-83,-21),(83,21)).arc((-1,59),(-83,21)).close().assemble().finalize().extrude(114).union(w1.sketch().segment((-100,-21),(-83,-21)).arc((-79,0),(-72,21)).segment((-100,21)).close().assemble().finalize().extrude(-45))