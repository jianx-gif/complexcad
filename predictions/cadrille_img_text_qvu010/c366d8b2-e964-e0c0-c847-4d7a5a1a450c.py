import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((-80,19),(-45,-1),(-23,-34)).arc((23,-12),(33,-61)).arc((38,-69),(42,-77)).arc((31,27),(-80,19)).assemble().finalize().extrude(200)