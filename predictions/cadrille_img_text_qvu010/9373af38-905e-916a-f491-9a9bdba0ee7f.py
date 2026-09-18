import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
w1=cq.Workplane('XY',origin=(0,0,91))
r=w0.sketch().push([(-68,-14)]).circle(32).circle(31,mode='s').finalize().extrude(199).union(w1.sketch().arc((-100,-29),(-19,29),(33,-58)).arc((15,95),(-100,-29)).assemble().finalize().extrude(-182))