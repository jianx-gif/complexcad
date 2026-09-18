import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-14,0))
w1=cq.Workplane('XY',origin=(0,0,86))
r=w0.sketch().arc((-100,-58),(0,0),(-100,58)).close().assemble().finalize().extrude(34).union(w1.sketch().arc((-89,-12),(-75,-31),(-56,-45)).arc((-45,-66),(-23,-79)).arc((-18,-86),(-11,-92)).arc((-35,-66),(-53,-35)).arc((-61,-28),(-58,-18)).arc((-64,36),(-23,79)).arc((1,71),(23,57)).arc((45,40),(53,15)).arc((64,1),(58,-18)).arc((57,-28),(53,-37)).arc((51,-40),(50,-43)).arc((66,-31),(79,-12)).close().assemble().finalize().extrude(14))