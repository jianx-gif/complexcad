import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-67,-67))
r=w0.sketch().segment((29,-58),(29,-57)).segment((31,-57)).arc((34,-55),(37,-57)).segment((39,-57)).arc((34,-52),(29,-58)).assemble().finalize().extrude(134).union(w0.workplane(offset=134/2).moveTo(0,1).cylinder(134,2))