import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
w1=cq.Workplane('ZX',origin=(0,30,0))
r=w0 top in on (10,0))
w1=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().segment((-36,10),(-29,10)).segment((-29,11)).segment((-36,11)).close().assemble().finalize().extrude(-11).union(w0.sketch().segment((-36,10),(-28,10)).segment((-28,12)).segment((-36,12)).close().assemble().finalize().extrude(-11)).union(w0.sketch().segment((24,-29),(36,-10)).segment((36,16)).close().assemble().finalize().extrude(-2)).union(w0.sketch().segment((16,-34),(27,-26)).segment((25,-23)).close().assemble().finalize().extrude(-2))