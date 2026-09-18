import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,0))
w1 For (36,10))
w1 For (36,10))
w1 For (36,10))
w1 For (36,10))
r=w0 top0.sketch().segment((-100,14),(-99,13)).segment((-99,12)).segment((-98,12)).segment((-98,13)).segment((-100,13)).segment((-99,12)).segment((-99,11)).segment((-98,11)).segment((-99,12)).segment((-100,12)).segment((-99,11)).segment((-99,10)).segment((-98,10)).segment((-99,11)).segment((-100,11)).segment((-99,10)).segment((-99,11)).segment((-100,11)).segment((-99,12)).segment((-99,13)).close().assemble().finalize().extrude(-11).union(w0.sketch().segment((-10,10),(1,15)).segment((-1,17)).close().assemble().finalize().extrude(-7))
