import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,89,0))
w1=cq.Workplane('ZX',origin=(0,42,0))
r=w0.sketch().arc((-75,33),(74,-66),(-13,88)).arc((-46,65),(-75,33)).assemble().finalize().extrude(-148).union(w0.sketch().arc((-24,100),(-10,77),(1,52)).arc((10,51),(18,48)).arc((20,50),(22,52)).arc((10,77),(-13,95)).arc((-18,98),(-24,100)).assemble().finalize().extrude(-24)).union(w1.workplane(offset=-103/2).moveTo(10,0).cylinder(103,90))