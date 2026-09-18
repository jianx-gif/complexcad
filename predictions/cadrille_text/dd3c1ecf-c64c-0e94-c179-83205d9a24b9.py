import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-7,-7))
w1=cq.Workplane('XY',origin=(-100,-7,-7))
r=w0.sketch().segment((92,-1),(92,1)).arc((91,0),(92,-1)).assemble().finalize().extrude(15).union(w1.sketch().face(w1.sketch().segment((92,-1),(92,1)).segment((92,1),(93,1)).arc((93,1),(93,-1),(92,-1)).assemble()).finalize().extrude(14))