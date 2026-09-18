import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((92,-29),(100,-29)).segment((100,-29),(100,29)).segment((100,29),(92,29)).close().assemble().finalize().extrude(100).union(w0.sketch().segment((-100,29),(-92,29)).segment((-92,29),(-92,42)).arc((-96,36),(-100,29)).assemble().finalize().extrude(100))