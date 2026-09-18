import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,16))
w1=cq.Workplane('ZX',origin=(0,10,0))
r=w0.sketch().segment((-40,-10),(-33,-10)).segment((-33,-8)).segment((-40,-8)).close().assemble().finalize().extrude(-17).union(w0.sketch().segment((-34,10),(-33,10)).segment((-33,11)).segment((-34,11)).close().assemble().finalize().extrude(-16)).union(w0.sketch().segment((15,-10),(45,-10)).segment((45,-5)).segment((15,-5)).close().assemble().finalize().extrude(-16)).union(w0.sketch().segment((15,10),(15,11)).segment((16,11)).arc((10,10),(16,10)).close().assemble().finalize().extrude(-16))