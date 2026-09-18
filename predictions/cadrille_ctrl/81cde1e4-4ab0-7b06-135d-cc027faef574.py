import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,6))
r=w0.sketch().segment((-40,-15),(-10,-15)).arc((-25,0),(-10,15)).segment((-40,15)).close().assemble().reset().face(w0.sketch().segment((10,-15),(40,-15)).segment((40,15)).segment((10,15)).arc((25,0),(10,-15)).assemble()).finalize().extrude(-6).union(w0.sketch().segment((-13,-3),(13,-3)).segment((13,3)).segment((11,3)).segment((11,1)).segment((9,1)).segment((9,3)).segment((-13,3)).close().assemble().finalize().extrude(-6)).union(w0.workplane(offset=8/2).cylinder(8,14))
