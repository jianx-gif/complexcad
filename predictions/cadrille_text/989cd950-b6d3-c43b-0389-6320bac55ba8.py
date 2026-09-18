import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((92,-49),(100,-49)).segment((100,-47)).segment((94,-47)).arc((93,-48),(92,-49)).assemble().finalize().extrude(100)