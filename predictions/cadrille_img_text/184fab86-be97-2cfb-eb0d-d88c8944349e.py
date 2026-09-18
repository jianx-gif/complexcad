import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,97,0))
w1=cq.Workplane('XY',origin=(0,0,-91))
r=w0.sketch().arc((-100,-39),(0,39),(100,-39)).segment((100,-29)).arc((0,35),(-100,-29)).close().assemble().finalize().extrude(-195).union(w1.workplane(offset=163/2).moveTo(0,2).cylinder(163,39))