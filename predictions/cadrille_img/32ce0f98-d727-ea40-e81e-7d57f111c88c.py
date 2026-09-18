import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((-44,-79),(15,-26),(44,49)).segment((44,79)).arc((11,36),(-18,-10)).arc((-25,-14),(-31,-19)).arc((-37,-24),(-44,-29)).close().assemble().finalize().extrude(-200).union(w0.sketch().arc((-24,-73),(18,0),(-24,73)).close().assemble().finalize().extrude(-185))