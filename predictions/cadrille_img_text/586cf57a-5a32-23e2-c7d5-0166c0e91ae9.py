import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-25,0))
w1=cq.Workplane('ZX',origin=(0,-77,0))
r=w0.sketch().arc((-74,46),(-60,58),(-44,67)).segment((-44,72)).segment((-29,72)).arc((0,79),(29,72)).segment((44,72)).segment((44,67)).arc((60,58),(74,46)).arc((0,100),(-74,46)).assemble().finalize().extrude(100).union(w1.sketch().arc((-35,-18),(0,-39),(35,-18)).segment((59,-18)).segment((59,18)).segment((35,18)).arc((0,39),(-35,18)).segment((-11,18)).segment((-11,-18)).close().assemble().finalize().extrude(-13))