import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,15,0))
w1=cq.Workplane('ZX',origin=(0,50,0))
r=w0.sketch().segment((-50,52),(50,50)).arc((0,99),(-50,52)).assemble().finalize().extrude(-15).union(w1.sketch().segment((0,-100),(13,-100)).arc((14,-97),(15,-100)).segment((20,-100)).segment((20,100)).segment((0,100)).close().assemble().push([(12,74)]).circle(7,mode='s').finalize().extrude(-100))