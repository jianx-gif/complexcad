import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-97,0))
w1=cq.Workplane('ZX',origin=(0,-70,0))
r=w0.sketch().arc((-100,22),(-5,-10),(90,22)).segment((84,22)).arc((-5,-8),(-94,22)).close().assemble().reset().face(w0.sketch().arc((95,22),(98,20),(100,17)).segment((100,22)).close().assemble()).finalize().extrude(195).union(w1.sketch().arc((-22,-36),(52,31),(-22,99)).segment((-22,36)).arc((-10,31),(-22,27)).close().assemble().finalize().extrude(109))