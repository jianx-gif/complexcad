import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('ZX',origin=(0,49,0))
r=w0.sketch().segment((-80,-16),(-77,-18)).arc((-75,-26),(-72,-34)).segment((-72,-50)).segment((-63,-50)).arc((0,-78),(63,-50)).segment((72,-50)).segment((72,-34)).arc((78,-1),(72,32)).segment((72,48)).segment((63,48)).arc((0,78),(-63,48)).segment((-72,48)).segment((-72,32)).arc((-78,8),(-77,-15)).close().assemble().finalize().extrude(-199).union(w1.sketch().circle(100).circle(94,mode='s').finalize().extrude(-123))