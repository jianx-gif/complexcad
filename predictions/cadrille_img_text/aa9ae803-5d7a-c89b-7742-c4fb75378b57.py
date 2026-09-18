import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,95,0))
w1=cq.Workplane('ZX',origin=(0,90,0))
r=w0.sketch().arc((-4,-86),(1,-87),(4,-88)).segment((4,-86)).close().assemble().finalize().extrude(-190).union(w0.sketch().arc((-4,-86),(88,-43),(79,57)).arc((-75,57),(-4,-86)).assemble().finalize().extrude(-162)).union(w1.sketch().push([(1,5)]).circle(85).circle(70,mode='s').finalize().extrude(-156))