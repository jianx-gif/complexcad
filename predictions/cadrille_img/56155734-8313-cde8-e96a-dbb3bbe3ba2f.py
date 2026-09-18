import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-49,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-69,-59),(-66,-57),(-62,-55)).arc((-85,21),(-30,78)).arc((-33,83),(-36,88)).arc((-99,16),(-69,-59)).assemble().finalize().extrude(129).union(w1.sketch().arc((-65,-59),(15,40),(100,-62)).segment((100,20)).segment((88,20)).arc((0,73),(-88,20)).segment((-65,20)).close().assemble().finalize().extrude(24))