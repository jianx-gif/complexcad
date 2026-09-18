import cadquery as cq
w0=cq.Workplane('YZ',origin=(65,0,0))
w1=cq.Workplane('ZX',origin=(0,68,0))
r=w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(35).union(w1.sketch().arc((-43,-87),(-10,-59),(1,-100)).arc((30,95),(-43,-87)).assemble().finalize().extrude(-161))