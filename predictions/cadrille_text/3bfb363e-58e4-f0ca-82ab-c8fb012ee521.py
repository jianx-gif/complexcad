import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-37))
r=w0.sketch().segment((-90,49),(-89,49)).segment((-89,50)).close().assemble().reset().face(w0.sketch().segment((89,-50),(90,-49)).segment((89,-49)).close().assemble()).finalize().extrude(74).union(w0.workplane(offset=74/2).cylinder(74,5))