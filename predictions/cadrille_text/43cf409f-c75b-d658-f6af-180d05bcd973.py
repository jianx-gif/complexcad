import cadquery as cq
w0=cq.Workplane('ZX',origin=(-100,100,0))
w1=cq.Workplane('ZX',origin=(-100,100,0))
r=w0.sketch().segment((-41,-48),(-39,-48)).segment((-41,-46)).close().assemble().finalize().extrude(-118).union(w1.sketch().face(w1.sketch().segment((0,2),(0,4)).arc((-1,10),(0,15)).segment((0,17)).arc((-1,20),(0,23)).segment((0,25)).arc((-1,22),(0,20)).segment((0,22)).arc((-1,20),(0,18)).segment((0,20)).arc((-1,18),(0,17)).segment((0,15)).arc((-1,10),(0,2)).assemble()).finalize().extrude(-200))