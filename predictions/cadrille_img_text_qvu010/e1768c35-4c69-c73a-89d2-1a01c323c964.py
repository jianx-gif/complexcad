import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-45,0))
w1=cq.Workplane('ZX',origin=(0,-90,0))
r=w0.sketch().arc((-100,72),(-5,70),(78,18)).segment((88,18)).segment((88,-18)).segment((83,-18)).arc((83,-34),(79,-50)).arc((88,-54),(88,-63)).arc((94,-49),(97,-34)).segment((100,-34)).segment((100,34)).segment((97,34)).arc((1,100),(-100,72)).assemble().finalize().extrude(130).union(w1.sketch().arc((-34,-34),(0,5),(34,34)).segment((34,34),(34,45)).arc((-19,59),(-34,10)).close().assemble().finalize().extrude(-2))