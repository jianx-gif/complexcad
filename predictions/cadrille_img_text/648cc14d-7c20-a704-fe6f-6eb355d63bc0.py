import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-58,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((84,-49),(94,-36),(100,-21)).segment((84,-21)).close().assemble().finalize().extrude(156).union(w1.sketch().arc((-60,-59),(0,-68),(60,-59)).segment((60,-58)).arc((0,-65),(-60,-58)).close().assemble().finalize().extrude(200))