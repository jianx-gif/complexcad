import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-47,-11))
r=w0.sketch().segment((94,-52),(100,-52)).segment((100,-47)).arc((97,-49),(94,-52)).assemble().finalize().extrude(31).union(w0.workplane(offset=111/2).moveTo(0,-45).box(12,10,111))