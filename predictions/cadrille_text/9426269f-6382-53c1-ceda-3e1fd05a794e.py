import cadquery as cq
w0=cq.Workplane('ZX',origin=(-100,33,-1))
w1=cq.Workplane('ZX',origin=(-100,33,-1))
r=w0.sketch().segment((95,-58),(95,100)).arc((39,21),(95,-58)).assemble().finalize().extrude(-34).union(w1.workplane(offset=-67/2).moveTo(0,21).cylinder(67,3))