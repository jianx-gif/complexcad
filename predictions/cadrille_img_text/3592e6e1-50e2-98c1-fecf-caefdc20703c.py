import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-69,-59),(69,-59)).segment((69,-35)).arc((0,-68),(-69,-35)).close().assemble().finalize().extrude(200).union(w0.sketch().arc((-65,20),(0,41),(65,20)).segment((65,59)).segment((-65,59)).close().assemble().finalize().extrude(200))