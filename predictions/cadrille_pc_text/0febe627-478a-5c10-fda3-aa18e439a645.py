import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,71,0))
w1=cq.Workplane('ZX',origin=(0,76,0))
r=w0.sketch().segment((-14,-95),(14,-95)).segment((14,100)).segment((12,100)).segment((12,95)).segment((-14,95)).close().assemble().finalize().extrude(-147).union(w1.sketch().rect(20,72).circle(3,mode='s').finalize().extrude(-147))