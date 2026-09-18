import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,89,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-86,-18),(86,18)).arc((0,50),(-86,18)).assemble().finalize().extrude(-109).union(w1.sketch().segment((-97,-27),(97,-27)).segment((97,27)).segment((-97,27)).segment((-97,-22)).segment((-94,-22)).segment((-94,-26)).segment((-97,-26)).close().assemble().finalize().extrude(-200))