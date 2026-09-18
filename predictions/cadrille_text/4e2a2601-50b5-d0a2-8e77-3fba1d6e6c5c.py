import cadquery as cq
w0=cq.Workplane('XY',origin=(-33,-11,-100))
w1=cq.Workplane('XY',origin=(-33,-11,-100))
r=w0.sketch().segment((99,11),(99,12)).arc((96,10),(99,11)).assemble().finalize().extrude(200).union(w1.sketch().face(w1.sketch().segment((0,0),(67,0)).segment((67,0),(67,22)).segment((67,22),(0,22)).segment((0,22),(0,0)).assemble()).finalize().extrude(110))