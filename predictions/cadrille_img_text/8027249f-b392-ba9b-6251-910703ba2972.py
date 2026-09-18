import cadquery as cq
w0=cq.Workplane('YZ',origin=(-57,0,0))
w1=cq.Workplane('ZX',origin=(0,38,0))
r=w0.sketch().arc((-52,62),(-46,43),(-37,25)).segment((-37,28)).segment((-32,28)).arc((-41,44),(-46,62)).close().assemble().reset().face(w0.sketch().arc((37,-28),(46,-44),(46,-62)).segment((52,-62)).segment((52,-25)).arc((46,-43),(37,-62)).close().assemble()).finalize().extrude(135).union(w1.sketch().segment((-77,-47),(57,-47)).arc((65,-37),(77,-31)).segment((77,47)).segment((-77,47)).close().assemble().finalize().extrude(-25))