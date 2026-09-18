import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-34,0))
w1=cq.Workplane('ZX',origin=(0,-59,0))
r=w0.sketch().segment((-70,-1),(-69,-1)).arc((0,-69),(69,-1)).segment((70,-1)).segment((70,1)).segment((69,1)).arc((0,69),(-69,1)).segment((-70,1)).close().assemble().finalize().extrude(109).union(w1.sketch().segment((-49,-57),(-44,-57)).arc((10,-72),(64,-57)).segment((69,-57)).segment((69,-54)).arc((100,14),(69,81)).segment((69,84)).segment((64,84)).arc((10,99),(-44,84)).segment((-49,84)).segment((-49,81)).arc((-80,14),(-49,-54)).close().assemble().finalize().extrude(111))