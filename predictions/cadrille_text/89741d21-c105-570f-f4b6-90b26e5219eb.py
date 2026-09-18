import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-67,-67))
r=w0.sketch().segment((27,-57),(27,-56)).segment((30,-56)).arc((34,-53),(38,-56)).segment((41,-56)).arc((34,-49),(27,-57)).assemble().finalize().extrude(133).union(w0.workplane(offset=133/2).moveTo(0,10).cylinder(133,3))