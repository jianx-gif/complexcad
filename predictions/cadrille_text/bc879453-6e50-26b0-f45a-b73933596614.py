import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-10,-10))
r=w0.sketch().segment((92,-11),(92,-9)).segment((95,-9)).arc((98,-7),(99,-9)).segment((100,-9)).arc((98,-6),(95,-5)).arc((95,-7),(94,-5)).arc((93,-7),(94,-9)).segment((94,-11)).close().assemble().finalize().extrude(20)