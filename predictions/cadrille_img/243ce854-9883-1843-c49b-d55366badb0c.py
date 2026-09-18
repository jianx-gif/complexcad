import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.workplane(offset=-200/2).moveTo(5,8).cylinder(200,87).union(w0.sketch().arc((-84,-1),(-79,-23),(-69,-43)).close().assemble().reset().face(w0.sketch().arc((-55,-66),(0,-84),(55,-66)).close().assemble()).reset().face(w0.sketch().segment((-55,66),(55,66)).arc((0,84),(-55,66)).assemble()).finalize().extrude(-197))