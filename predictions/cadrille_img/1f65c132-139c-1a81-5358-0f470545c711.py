import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,73))
w1=cq.Workplane('ZX',origin=(0,-42,0))
r=w0.sketch().segment((-85,-11),(-27,-11)).arc((0,-23),(27,-11)).segment((85,-11)).segment((85,11)).segment((27,11)).arc((0,23),(-27,11)).segment((-85,11)).close().assemble().finalize().extrude(-116).union(w1.sketch().segment((-100,-33),(-79,-33)).arc((0,34),(79,-33)).segment((100,-33)).segment((100,33)).segment((79,33)).arc((0,80),(-79,33)).segment((-100,33)).close().assemble().finalize().extrude(125))