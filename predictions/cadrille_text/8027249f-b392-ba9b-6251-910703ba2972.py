import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-11))
r=w0.sketch().segment((92,-44),(92,-38)).segment((97,-38)).arc((98,-36),(99,-38)).segment((99,-44)).close().assemble().finalize().extrude(-8).union(w0.workplane(offset=28/2).cylinder(28,3))