import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
w1=cq.Workplane('ZX',origin=(0,20,0))
r=w0 The ( (36,10))
w1 For does f The (30,10))
w1 For (36,10))
w1 For has Forr=w0.sketch().segment((-38,10),(-36,10)).segment((-36,11)).segment((-38,11)).close().assemble().finalize().extrude(-11).union(w0.sketch().segment((-36,10),(-35,10)).segment((-35,11)).segment((-36,11)).segment((-36,10)).segment((-35,10)).segment((-35,12)).segment((-36,12)).close().assemble().finalize().extrude(-1))
