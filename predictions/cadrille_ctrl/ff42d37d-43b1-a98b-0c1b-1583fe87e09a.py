import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,10,0))
w1=cq.Workplane('YZ',origin=(24,0))
r=w0 topun ( (36,10))
w1 On (30,10))
w1 On con The ( (36,10))
w1 On con (36,10))
r=w0.sketch().segment((-100,10),(-99,9)).segment((-99,10)).segment((-98,10)).segment((-98,12)).segment((-100,12)).segment((-100,11)).segment((-99,11)).segment((-99,10)).segment((-98,10)).segment((-98,12)).segment((-100,12)).segment((-100,11)).segment((-99,11)).segment((-99,10)).segment((-98,10)).segment((-98,12)).segment((-99,12)).segment((-99,11)).segment((-100,11)).segment((-100,10)).segment((-99,10)).segment((-99,9)).segment((-100,9)).close().assemble().finalize().extrude(-11).union(w0.sketch().segment((-11,10),(16,10)).segment((16,16)).segment((-11,16)).close().assemble().finalize().extrude(-1))
