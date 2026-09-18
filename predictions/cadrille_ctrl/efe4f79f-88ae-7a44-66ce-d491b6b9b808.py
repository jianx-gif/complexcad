import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,5))
r=w0.workplane(offset=-5/2).cylinder(5,7).union(w0.sketch().segment((-15,-10),(-11,-10)).arc((-14,0),(-11,10)).segment((-15,10)).close().assemble().reset().face(w0.sketch().segment((11,-10),(15,-10)).segment((15,3)).arc((14,-3),(11,-10)).assemble()).finalize().extrude(95))
