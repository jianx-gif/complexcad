import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('XY',origin=(0,0,91))
r=w0.sketch().segment((-100,-99),(100,-99)).segment((100,20)).segment((89,65)).segment((89,-10)).segment((10,-10)).arc((0,-12),(-10,-10)).segment((-100,-10)).close().assemble().finalize().extrude(-148).union(w1.sketch().segment((-75,-28),(-68,-28)).arc((0,-81),(68,-28)).segment((75,-28)).segment((75,28)).segment((68,28)).arc((0,81),(-68,28)).segment((-75,28)).close().assemble().finalize().extrude(-183))