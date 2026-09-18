import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-83))
r=w0.sketch().segment((29,-58),(29,-57)).segment((31,-57)).arc((35,-52),(40,-57)).segment((42,-57)).arc((35,-49),(29,-58)).assemble().finalize().extrude(167).union(w0.workplane(offset=167/2).moveTo(0,1).cylinder(167,3))