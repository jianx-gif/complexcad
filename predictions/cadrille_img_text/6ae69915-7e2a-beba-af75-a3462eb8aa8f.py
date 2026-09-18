import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,35,0))
r=w0.sketch().arc((-50,54),(42,13),(66,-76)).arc((75,65),(-50,54)).assemble().finalize().extrude(-71).union(w0.sketch().segment((-40,55),(-29,55)).arc((15,-53),(59,55)).segment((67,55)).segment((67,65)).segment((47,65)).arc((15,78),(-18,65)).segment((-40,65)).close().assemble().finalize().extrude(3))