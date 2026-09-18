import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((-30,-50),(17,-49),(64,-32)).segment((64,-23)).close().assemble().reset().face(w0.sketch().segment((-30,50),(74,23)).arc((27,49),(-30,32)).close().assemble()).finalize().extrude(200).union(w0.workplane(offset=200/2).moveTo(-39,0).box(90,10,200))