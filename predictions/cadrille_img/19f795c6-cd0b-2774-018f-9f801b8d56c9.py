import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-11,0))
w1=cq.Workplane('XY',origin=(0,0,-96))
r=w0.sketch().arc((-100,-1),(0,-100),(100,-1)).segment((78,-1)).arc((0,-78),(-78,-1)).close().assemble().reset().face(w0.sketch().segment((-100,1),(-78,1)).arc((0,78),(78,1)).segment((100,1)).arc((0,78),(-100,1)).assemble()).finalize().extrude(48).union(w1.sketch().arc((-29,-78),(0,-69),(29,-78)).segment((29,-65)).arc((70,0),(29,65)).segment((29,52)).arc((0,60),(-29,52)).segment((-29,65)).arc((-70,0),(-29,-65)).close().assemble().finalize().extrude(196))