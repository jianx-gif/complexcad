import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-28,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-83,-5),(-60,-5)).arc((0,-60),(60,-5)).segment((83,-5)).segment((83,5)).segment((60,5)).arc((0,60),(-60,5)).segment((-83,5)).close().assemble().finalize().extrude(117).union(w1.sketch().arc((-99,-17),(0,-100),(99,-17)).segment((60,-17)).arc((0,-62),(-60,-17)).close().assemble().finalize().extrude(195))