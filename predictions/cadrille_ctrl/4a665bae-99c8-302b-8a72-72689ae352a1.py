import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,10,0))
w1=cq.Workplane('YZ',origin=(-15,0,0))
r=w0.sketch().segment((1,10),(1,11)).segment((2,11)).arc((-1,10),(2,10)).close().assemble().finalize().extrude(-20).union(w0.sketch().segment((3,10),(11,10)).segment((11,15)).arc((7,12),(3,10)).assemble().finalize().extrude(-20)).union(w1.sketch().segment((-10,47),(10,47)).segment((10,60)).arc((1,57),(-10,60)).close().assemble().finalize().extrude(30))
