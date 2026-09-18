import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,5))
r=w0.workplane(offset=-5/2).cylinder(5,7).union(w0.sketch().segment((-15,-10),(-9,-10)).arc((-14,0),(-9,10)).segment((-15,10)).close().assemble().reset().face(w0.sketch().segment((9,-10),(15,-10)).segment((15,3)).arc((13,3),(10,4)).arc((10,-3),(9,-10)).assemble()).finalize().extrude(95))