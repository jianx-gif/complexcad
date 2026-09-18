import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('ZX',origin=(0,86,0))
r=w0.sketch().arc((-99,-16),(0,-91),(99,-16)).segment((87,-16)).arc((0,-88),(-87,-16)).close().assemble().reset().face(w0.sketch().segment((-99,16),(-87,16)).arc((0,88),(87,16)).segment((99,16)).arc((0,91),(-99,16)).assemble()).finalize().extrude(-158).union(w1.sketch().circle(100).circle(89,mode='s').finalize().extrude(-153))