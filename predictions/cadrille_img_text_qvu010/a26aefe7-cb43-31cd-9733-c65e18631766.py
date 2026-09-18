import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-34,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-87,66),(-86,66)).segment((-86,67)).close().assemble().finalize().extrude(48).union(w0.sketch().segment((-65,1),(-64,1)).segment((-64,2)).close().assemble().reset().face(w0.sketch().segment((-24,1),(87,-25)).arc((35,10),(-24,1)).assemble()).finalize().extrude(119)).union(w1.sketch().arc((-86,-35),(-84,-36),(-82,-38)).segment((47,-38)).arc((54,-27),(64,-18)).segment((64,38)).segment((-86,38)).close().assemble().finalize().extrude(200))