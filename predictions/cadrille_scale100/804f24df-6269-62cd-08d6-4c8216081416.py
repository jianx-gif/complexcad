import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('ZX',origin=(0,9,0))
r=w0.sketch().segment((30,0),(30,70)).segment((51,70)).arc((53,72),(55,73)).arc((11,91),(30,47)).segment((30,92)).arc((10,47),(30,0)).assemble().finalize().extrude(21).union(w1.sketch().segment((0,10),(5,10)).arc((13,0),(24,6)).arc((27,6),(30,7)).segment((30,30)).segment((0,30)).close().assemble().finalize().extrude(86))