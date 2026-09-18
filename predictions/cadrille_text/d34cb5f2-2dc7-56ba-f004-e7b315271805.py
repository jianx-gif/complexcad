import cadquery as cq
w0=cq.Workplane('XY',origin=(-50,-50,-100))
w1=cq.Workplane('XY',origin=(-50,-50,-100))
r=w0.sketch().segment((45,-42),(45,42)).arc((11,0),(45,-42)).assemble().finalize().extrude(200).union(w1.workplane(offset=110/2).moveTo(0,50).cylinder(110,3))