import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,1,0))
r=w0.sketch().arc((-21,-62),(0,-65),(21,-62)).close().assemble().reset().face(w0.sketch().segment((-21,62),(21,62)).arc((0,65),(-21,62)).assemble()).finalize().extrude(-10).union(w0.sketch().arc((1,-75),(0,-77),(2,-78)).arc((-58,76),(100,1)).arc((97,2),(95,3)).arc((-61,74),(1,-75)).assemble().finalize().extrude(9))