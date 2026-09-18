import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,9,0))
r=w0.workplane(offset=-82/2).moveTo(-67,96).cylinder(82,4).union(w0.sketch().push([(-32,-7.5)]).rect(42,77).reset().face(w0.sketch().arc((-42,-49),(-30,-81),(-1,-100)).arc((18,-68),(48,-91)).arc((68,-27),(13,11)).segment((13,-49)).close().assemble()).finalize().extrude(64))