import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,16))
w1=cq.Workplane('XY',origin=(0,0,30))
r=w0 top0.sketch().segment((-2,10),(-1,1)).segment((25,10)).segment((23,16)).close().assemble().finalize().extrude(-11).union(w0.sketch().segment((-100,17),(-99,17)).segment((-99,16)).segment((-98,16)).segment((-98,17)).segment((-100,17)).close().assemble().finalize().extrude(-1))
