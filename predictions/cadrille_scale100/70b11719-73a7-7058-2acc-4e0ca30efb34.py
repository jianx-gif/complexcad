import cadquery as cq
w0=cq.Workplane('YZ',origin=(18,0))
w1=cq.Workplane('XY',origin=(0,0,8))
r=w0 top in on (10,0))
w1=cq.Workplane('ZX',origin=(0,14,0))
r=w0.sketch().segment((-3,10),(-1,10)).segment((-1,10)).segment((-2,10)).segment((-2,8)).segment((-3,8)).close().assemble().finalize().extrude(-3).union(w0.sketch().segment((-3,10),(-1,10)).segment((-1,11)).segment((-3,11)).close().assemble().finalize().extrude(-13)).union(w0.sketch().segment((-3,10),(-1,10)).segment((-1,12)).segment((-3,12)).close().assemble().finalize().extrude(-13)).union(w0.sketch().segment((-3,10),(-1,10)).segment((-1,12)).segment((-3,12)).close().assemble().finalize().extrude(-12)).union(w0.sketch().segment((-100,1),(-99,-1)).segment((-99,0)).segment((-98,0)).segment((-98,1)).segment((-97,1)).segment((-97,0)).segment((-96,0)).segment((-97,1)).segment((-99,1)).segment((-99,0)).close().assemble().finalize().extrude(-11))