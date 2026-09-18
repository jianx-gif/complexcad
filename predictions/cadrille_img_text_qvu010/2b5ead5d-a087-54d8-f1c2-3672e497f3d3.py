import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,54))
w1=cq.Workplane('YZ',origin=(-88,0,0))
r=w0.sketch().arc((-55,-52),(0,-71),(55,-52)).segment((55,-1)).segment((55,1)).segment((55,52)).segment((-55,52)).segment((-55,1)).segment((-55,-1)).close().assemble().finalize().extrude(-110).union(w1.sketch().arc((10,-100),(45,-92),(71,-68)).arc((87,1),(71,68)).arc((45,92),(10,100)).segment((10,68)).arc((-15,1),(10,-68)).close().assemble().finalize().extrude(177))