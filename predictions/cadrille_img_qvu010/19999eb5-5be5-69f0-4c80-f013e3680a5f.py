import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-92))
w1=cq.Workplane('ZX',origin=(0,-14,0))
r=w0.sketch().arc((-87,-12),(-72,-31),(-52,-45)).close().assemble().reset().face(w0.sketch().segment((-38,45),(38,12)).arc((23,31),(2,45)).close().assemble()).reset().face(w0.sketch().arc((-3,-45),(23,-31),(38,-12)).close().assemble()).reset().face(w0.sketch().segment((52,45),(87,-12)).arc((72,11),(52,25)).close().assemble()).finalize().extrude(184).union(w1.sketch().segment((-100,-60),(-60,-60)).arc((-89,0),(-60,60)).segment((-100,60)).close().assemble().finalize().extrude(37))