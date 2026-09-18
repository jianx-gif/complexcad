import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-11))
r=w0.sketch().segment((92,-49),(100,-49)).segment((100,-47)).segment((94,-47)).arc((93,-48),(92,-49)).assemble().finalize().extrude(33).union(w0.sketch().segment((92,-49),(92,-47)).segment((94,-47)).arc((99,-48),(99,-44)).arc((98,-45),(97,-45)).arc((96,-47),(94,-48)).segment((94,-49)).close().assemble().finalize().extrude(62))