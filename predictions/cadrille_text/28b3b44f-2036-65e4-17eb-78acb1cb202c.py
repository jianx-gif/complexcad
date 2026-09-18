import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((27,-38),(27,-30)).arc((24,-23),(27,-16)).segment((27,38)).arc((11,0),(27,-38)).assemble().finalize().extrude(99).union(w0.sketch().segment((92,-38),(92,38)).arc((100,0),(92,-38)).assemble().finalize().extrude(100))