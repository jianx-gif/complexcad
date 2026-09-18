import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,96,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((-69,39),(-67,37),(-65,36)).arc((-66,38),(-69,39)).assemble().finalize().extrude(-192).union(w0.sketch().arc((-92,-40),(0,-95),(92,-40)).segment((67,-40)).arc((0,-78),(-67,-40)).close().assemble().reset().face(w0.sketch().segment((-92,40),(-67,40)).arc((0,78),(67,40)).segment((92,40)).arc((0,95),(-92,40)).assemble()).finalize().extrude(-186)).union(w1.sketch().arc((-49,-62),(0,-78),(49,-62)).segment((33,-62)).arc((0,-71),(-33,-62)).close().assemble().finalize().extrude(-196))