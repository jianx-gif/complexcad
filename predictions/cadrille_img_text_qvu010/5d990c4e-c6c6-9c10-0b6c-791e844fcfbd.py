import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().circle(99).circle(83,mode='s').finalize().extrude(27).union(w0.sketch().arc((-99,-34),(0,-76),(99,-34)).segment((90,-34)).arc((0,-74),(-90,-34)).close().assemble().reset().face(w0.sketch().segment((-99,34),(-90,34)).arc((0,74),(90,34)).segment((99,34)).arc((0,76),(-99,34)).assemble()).finalize().extrude(200))