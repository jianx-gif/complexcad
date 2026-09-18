import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,87,0))
w1=cq.Workplane('ZX',origin=(0,50,0))
r=w0.sketch().arc((-51,-39),(1,-75),(54,-43)).arc((57,-39),(60,-34)).arc((62,33),(4,75)).arc((-94,43),(-51,-39)).assemble().finalize().extrude(-10).union(w0.sketch().arc((-100,16),(89,-52),(-46,89)).arc((29,-19),(-100,16)).assemble().finalize().extrude(-10)).union(w1.workplane(offset=-100/2).cylinder(100,92))