import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,91,0))
r=w0.sketch().segment((-97,-54),(57,-58)).arc((59,-54),(61,-50)).segment((-97,-46)).close().assemble().finalize().extrude(200).union(w1.sketch().arc((-100,-46),(-34,-16),(33,-20)).arc((38,-10),(45,-1)).arc((50,24),(68,44)).arc((70,46),(72,49)).arc((-29,73),(-100,7)).close().assemble().finalize().extrude(-182))