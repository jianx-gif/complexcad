import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-25,0))
w1=cq.Workplane('ZX',origin=(0,-10,0))
r=w0.sketch().segment((12,72),(15,74)).arc((-14,-73),(20,73)).segment((23,67)).segment((16,63)).close().assemble().finalize().extrude(10).union(w0.sketch().arc((19,53),(33,39),(42,22)).segment((45,22)).segment((45,16)).arc((47,10),(49,4)).segment((52,0)).arc((42,32),(19,53)).assemble().finalize().extrude(83)).union(w1.sketch().push([(12,13)]).circle(87).circle(33,mode='s').finalize().extrude(-28))