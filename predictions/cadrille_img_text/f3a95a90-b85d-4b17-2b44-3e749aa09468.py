import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-45))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((-48,21),(-46,18),(-43,15)).arc((-35,13),(-31,6)).arc((10,19),(48,34)).arc((-2,35),(-48,21)).assemble().finalize().extrude(125).union(w1.sketch().arc((-87,-49),(0,-66),(87,-49)).segment((87,49)).arc((0,66),(-87,49)).close().assemble().finalize().extrude(200))