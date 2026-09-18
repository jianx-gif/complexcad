import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-56))
w1=cq.Workplane('ZX',origin=(0,-5,0))
r=w0.sketch().arc((-86,-98),(0,-80),(86,-58)).arc((-11,-70),(-86,-98)).assemble().finalize().extrude(-10).union(w1.sketch().arc((-55,-46),(45,-71),(100,15)).arc((25,-59),(-55,-46)).assemble().finalize().extrude(-10))