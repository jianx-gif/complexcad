import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,29,0))
w1=cq.Workplane('ZX',origin=(0,19,0))
r=w0.sketch().arc((-49,72),(-36,63),(-24,53)).arc((59,39),(49,-44)).arc((56,-51),(62,-59)).arc((68,68),(-49,72)).assemble().push([(24,27)]).circle(39,mode='s').circle(24).finalize().extrude(-67).union(w0.sketch().segment((-44,69),(78,-37)).segment((78,-3)).arc((16,27),(-10,91)).arc((-27,82),(-44,69)).assemble().finalize().extrude(21)).union(w1.sketch().arc((-33,49),(46,39),(67,-38)).arc((70,66),(-33,49)).assemble().finalize().extrude(-31))