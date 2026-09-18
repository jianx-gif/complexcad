import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.workplane(offset=-200/2).moveTo(0,8).cylinder(200,89).union(w0.sketch().arc((-84,-39),(1,-89),(84,-39)).segment((74,-39)).arc((0,-85),(-74,-39)).close().assemble().reset().face(w0.sketch().segment((-84,39),(-74,39)).arc((0,85),(74,39)).segment((84,39)).arc((0,89),(-84,39)).assemble()).finalize().extrude(-197))