import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-1,-1))
r=w0.sketch().segment((92,-13),(92,-11)).segment((95,-11)).arc((98,-10),(100,-11)).arc((98,-10),(97,-10)).arc((96,-12),(94,-12)).arc((94,-13),(92,-13)).assemble().finalize().extrude(-13).union(w0.workplane(offset=1/2).moveTo(0,1).box(4,10,1))