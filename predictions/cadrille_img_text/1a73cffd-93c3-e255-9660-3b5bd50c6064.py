import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-60,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((-33,22),(-22,21),(-12,18)).arc((-10,31),(-4,43)).arc((-20,36),(-33,22)).assemble().finalize().extrude(126).union(w1.sketch().arc((-89,-57),(0,-80),(89,-57)).segment((89,-35)).arc((87,-32),(89,-29)).segment((89,57)).segment((-89,57)).close().assemble().push([(0,-46)]).circle(34,mode='s').finalize().extrude(200))