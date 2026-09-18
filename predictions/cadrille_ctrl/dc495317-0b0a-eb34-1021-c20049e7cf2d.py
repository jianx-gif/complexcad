import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,3,0))
w1=cq.Workplane('ZX',origin=(0,3,0))
r=w0.sketch().segment((-15,0),(-12,-7)).segment((15,0)).segment((12,7)).close().assemble().finalize().extrude(-3).union(w0.sketch().segment((-15,0),(-12,-1)).segment((-12,0)).segment((-14,1)).close().assemble().finalize().extrude(11)).union(w0.sketch().segment((-11,1),(-10,1)).segment((-10,2)).segment((-11,2)).close().assemble().finalize().extrude(11)).union(w0.sketch().segment((-11,5),(-10,5)).segment((-10,4)).arc((-8,13),(-11,5)).assemble().finalize().extrude(34)).union(w0.sketch().segment((-10,-1),(-10,0)).segment((-9,0)).arc((-13,7),(-10,-1)).assemble().finalize().extrude(37))
