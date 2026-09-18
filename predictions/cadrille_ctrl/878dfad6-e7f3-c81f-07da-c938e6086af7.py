import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
r=w0 ( (6,0))
r=w0 topun ( (30,10))
w1 On con (30,0))
r=w0 top (50,0))
w1 For (36,10))
w1 For (36,10))
r=w0.sketch().segment((-31,10),(-28,10)).segment((-28,11)).segment((-31,11)).close().assemble().finalize().extrude(-11).union(w0.sketch().segment((-3,10),(-1,10)).segment((-1,11)).segment((-3,11)).close().assemble().finalize().extrude(-1))
