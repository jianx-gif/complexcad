import cadquery as cq
w0=cq.Workplane('YZ',origin=(-50,0,0))
w1=cq.Workplane('ZX',origin=(0,-11,0))
r=w0.sketch().arc((-91,-10),(0,-71),(91,-10)).segment((89,-10)).arc((0,-69),(-89,-10)).close().assemble().reset().face(w0.sketch().segment((-91,10),(-89,10)).arc((0,69),(89,10)).segment((91,10)).arc((0,71),(-91,10)).assemble()).finalize().extrude(119).union(w1.sketch().segment((-99,-100),(99,-100)).segment((99,100)).segment((-87,100)).arc((-93,73),(-99,47)).close().assemble().finalize().extrude(48))