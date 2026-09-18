import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-31,-12))
r=w0.sketch().segment((91,-29),(100,-29)).segment((100,-27)).segment((92,-27)).arc((92,-28),(91,-29)).assemble().finalize().extrude(-38).union(w0.sketch().segment((-92,12),(-92,14)).arc((-93,21),(-92,29)).segment((-92,31)).arc((-97,21),(-92,12)).assemble().finalize().extrude(100))