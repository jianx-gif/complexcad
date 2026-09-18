import cadquery as cq
w0=cq.Workplane('YZ',origin=(95,0,0))
w1=cq.Workplane('ZX',origin=(0,-45,0))
r=w0.sketch().segment((-69,39),(-57,-36)).segment((-57,42)).close().assemble().reset().face(w0.sketch().segment((-48,-59),(-47,-62)).segment((-47,-59)).close().assemble()).reset().face(w0.sketch().segment((47,-42),(69,-39)).segment((57,36)).segment((57,-39)).close().assemble()).finalize().extrude(-195).union(w1.sketch().arc((-94,59),(-24,11),(1,-73)).arc((12,41),(-94,59)).assemble().finalize().extrude(134))