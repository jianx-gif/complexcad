import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-40,-2))
r=w0.sketch().segment((92,-39),(100,-39)).segment((100,-37)).segment((94,-37)).arc((93,-38),(92,-39)).assemble().finalize().extrude(40).union(w0.workplane(offset=44/2).moveTo(0,1).cylinder(44,3))