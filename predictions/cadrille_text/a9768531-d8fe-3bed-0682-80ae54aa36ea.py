import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-25,-11))
r=w0.sketch().segment((27,-58),(27,-57)).segment((30,-57)).segment((30,-58)).arc((32,-57),(34,-55)).segment((34,-54)).segment((35,-54)).arc((38,-52),(40,-54)).segment((41,-54)).segment((41,-55)).arc((43,-57),(44,-58)).close().assemble().finalize().extrude(-24).union(w0.workplane(offset=111/2).moveTo(0,1).cylinder(111,2))