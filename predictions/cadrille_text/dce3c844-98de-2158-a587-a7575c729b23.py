import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-6,-6))
r=w0.sketch().segment((92,-13),(92,-12)).segment((94,-12)).arc((98,-10),(99,-14)).segment((99,-15)).arc((98,-10),(92,-13)).assemble().finalize().extrude(-4).union(w0.sketch().segment((98,-14),(98,-12)).segment((100,-12)).arc((96,-10),(98,-14)).assemble().finalize().extrude(16))