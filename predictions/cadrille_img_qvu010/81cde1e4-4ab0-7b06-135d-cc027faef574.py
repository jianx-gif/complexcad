import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,21,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().circle(53).circle(16,mode='s').finalize().extrude(-54).union(w0.sketch().segment((-99,-4),(-63,-4)).arc((-64,0),(-63,4)).segment((-99,4)).close().assemble().reset().face(w0.sketch().segment((63,-4),(99,-4)).segment((99,4)).segment((63,4)).arc((64,0),(63,-4)).assemble()).finalize().extrude(67)).union(w1.sketch().arc((-79,19),(19,19),(-1,-79)).arc((43,46),(-79,19)).assemble().finalize().extrude(200))