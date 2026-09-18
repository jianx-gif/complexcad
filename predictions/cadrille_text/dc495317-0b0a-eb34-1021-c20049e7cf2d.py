import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((27,-58),(27,-57)).segment((30,-57)).arc((34,-54),(38,-57)).segment((41,-57)).arc((34,-52),(27,-58)).assemble().finalize().extrude(100).union(w0.workplane(offset=100/2).moveTo(0,1).cylinder(100,3))