import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-34))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-95,59),(33,-68)).segment((95,-5)).segment((-33,92)).close().assemble().finalize().extrude(134).union(w1.sketch().arc((-45,-92),(21,-71),(95,-54)).arc((20,-68),(-45,-92)).assemble().finalize().extrude(19))