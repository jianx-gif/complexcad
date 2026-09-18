import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-70,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-93,-4),(-88,-4)).arc((-87,19),(-79,41)).segment((-93,41)).close().assemble().reset().face(w0.sketch().segment((-78,-41),(-64,-41)).arc((-72,-30),(-78,-17)).close().assemble()).reset().face(w0.sketch().arc((-42,70),(-36,72),(-29,73)).segment((-29,93)).segment((-42,93)).close().assemble()).finalize().extrude(160).union(w1.sketch().circle(100).circle(96,mode='s').finalize().extrude(195))