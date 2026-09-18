import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-2))
w1=cq.Workplane('ZX',origin=(0,-11,0))
r=w0.workplane(offset=-14/2).moveTo(0,-19.5).box(200,61,14).union(w0.workplane(offset=30/2).moveTo(0,-1).cylinder(30,25)).union(w1.sketch().segment((-27,-83),(9,-83)).segment((9,-64)).segment((-1,-64)).arc((-10,-68),(-20,-64)).segment((-27,-64)).close().assemble().finalize().extrude(20))