import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((-45,-78),(14,-11),(45,78)).segment((39,72)).arc((10,-10),(-44,-66)).close().assemble().finalize().extrude(-200).union(w0.sketch().arc((-24,-78),(27,0),(-24,78)).close().assemble().finalize().extrude(-183))