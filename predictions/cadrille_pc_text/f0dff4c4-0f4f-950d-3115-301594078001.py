import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,20))
w1=cq.Workplane('XY',origin=(0,0,28))
r=w0.sketch().circle(100).circle(43,mode='s').finalize().extrude(-48).union(w1.sketch().arc((-89,-11),(-1,-1),(-11,-100)).arc((59,81),(-89,-11)).assemble().finalize().extrude(-11))