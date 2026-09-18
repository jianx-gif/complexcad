import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('ZX',origin=(0,9,0))
r=w0.sketch().segment((30,0),(30,70)).segment((51,70)).arc((53,72),(55,73)).arc((11,91),(30,47)).segment((30,92)).arc((1,47),(30,0)).assemble().finalize().extrude(30).union(w1.sketch().segment((21,0),(21,1)).segment((22,1)).arc((10,0),(22,0)).close().assemble().finalize().extrude(85))
