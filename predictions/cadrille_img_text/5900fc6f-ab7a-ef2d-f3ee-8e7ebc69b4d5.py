import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-69,33),(69,33)).arc((0,80),(-69,33)).assemble().finalize().extrude(10).union(w0.sketch().segment((-59,27),(20,-59)).segment((59,-27)).segment((-20,59)).close().assemble().finalize().extrude(185)).union(w0.sketch().segment((-89,19),(89,19)).arc((0,80),(-89,19)).assemble().finalize().extrude(200))