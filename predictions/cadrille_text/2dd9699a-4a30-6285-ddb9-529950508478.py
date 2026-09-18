import cadquery as cq
w0=cq.Workplane('ZX',origin=(-100,100,0))
r=w0.sketch().segment((-57,97),(-51,97)).segment((-51,100)).arc((-54,99),(-57,97)).assemble().finalize().extrude(-200)