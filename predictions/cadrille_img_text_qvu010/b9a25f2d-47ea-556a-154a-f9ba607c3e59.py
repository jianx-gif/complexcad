import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-58,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-92,1),(-85,1)).arc((0,-75),(85,1)).segment((92,1)).segment((92,9)).segment((85,9)).arc((0,75),(-85,9)).segment((-92,9)).close().assemble().finalize().extrude(136).union(w1.sketch().arc((-36,-52),(-19,-48),(-3,-42)).segment((-3,-58)).segment((3,-58)).segment((3,-38)).arc((19,-32),(36,-26)).segment((36,52)).segment((3,52)).segment((3,75)).segment((-3,75)).segment((-3,52)).segment((-36,52)).close().assemble().finalize().extrude(-34))