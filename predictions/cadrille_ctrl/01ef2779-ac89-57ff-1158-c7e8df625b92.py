import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,80))
r=w0.sketch().segment((-20,-15),(20,-15)).segment((20,15)).segment((-20,15)).segment((-20,10)).segment((-15,10)).segment((-15,14)).segment((-10,14)).segment((-10,10)).segment((15,10)).segment((15,-10)).segment((-15,-10)).segment((-15,-6)).segment((-20,-6)).close().assemble().finalize().extrude(-80).union(w0.sketch().segment((-15,-15),(15,-15)).segment((15,-10)).arc((0,-14),(-15,-10)).close().assemble().finalize().extrude(-79))
