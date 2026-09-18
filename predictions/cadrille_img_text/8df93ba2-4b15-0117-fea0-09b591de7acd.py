import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-25,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-79,-45),(-77,-45)).arc((10,-91),(97,-45)).segment((99,-45)).segment((99,-39)).arc((100,-1),(88,36)).segment((88,42)).segment((85,42)).arc((10,91),(-74,45)).segment((-79,45)).segment((-79,33)).arc((-84,0),(-79,-33)).close().assemble().finalize().extrude(45).union(w1.sketch().arc((-69,-29),(91,42),(-67,-33)).segment((-63,-33)).arc((90,42),(-69,-29)).assemble().finalize().extrude(200))