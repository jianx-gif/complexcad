import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-10,-10))
r=w0.sketch().segment((93,-13),(93,-10)).segment((95,-10)).arc((98,-7),(100,-10)).arc((98,-8),(99,-6)).arc((98,-5),(97,-5)).arc((97,-7),(95,-7)).arc((97,-10),(95,-13)).close().assemble().finalize().extrude(-8).union(w0.workplane(offset=28/2).cylinder(28,2))