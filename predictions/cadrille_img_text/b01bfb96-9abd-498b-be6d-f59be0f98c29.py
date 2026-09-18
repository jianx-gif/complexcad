import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('ZX',origin=(0,58,0))
r=w0.sketch().arc((-89,-36),(-81,-43),(-75,-51)).arc((81,59),(-89,-36)).assemble().finalize().extrude(-176).union(w0.sketch().arc((-45,-69),(0,-81),(45,-69)).close().assemble().reset().face(w0.sketch().segment((-45,69),(45,69)).arc((0,81),(-45,69)).assemble()).finalize().extrude(-176)).union(w1.sketch().circle(100).push([(10,14)]).circle(79,mode='s').finalize().extrude(-128))