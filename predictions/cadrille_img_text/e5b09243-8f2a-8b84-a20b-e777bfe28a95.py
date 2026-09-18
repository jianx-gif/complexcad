import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-63,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-74,58),(-69,58)).segment((-69,60)).segment((-65,60)).segment((-65,58)).segment((-62,58)).segment((-62,65)).segment((-74,65)).close().assemble().finalize().extrude(121).union(w1.sketch().arc((-100,19),(-59,33),(-16,33)).arc((-16,35),(-14,35)).arc((45,48),(100,29)).arc((100,30),(100,32)).arc((-1,58),(-100,65)).close().assemble().finalize().extrude(200))