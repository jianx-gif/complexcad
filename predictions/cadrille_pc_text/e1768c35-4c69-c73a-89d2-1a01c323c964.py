import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,53))
w1=cq.Workplane('ZX',origin=(0,-43,0))
r=w0.sketch().segment((-100,60),(-95,48)).arc((22,40),(63,-56)).segment((76,-32)).segment((66,-26)).arc((34,47),(-45,62)).segment((-48,76)).segment((-54,74)).segment((-51,61)).arc((-55,61),(-59,60)).segment((-61,73)).close().assemble().finalize().extrude(-109).union(w1.sketch().segment((-55,63),(55,63)).arc((0,100),(-55,63)).assemble().finalize().extrude(-33))