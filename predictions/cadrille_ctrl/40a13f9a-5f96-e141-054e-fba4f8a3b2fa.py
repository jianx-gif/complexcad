import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,42))
r=w0.sketch().arc((13,-2),(15,0),(13,2)).close().assemble().finalize().extrude(-92).union(w0.sketch().circle(30).reset().face(w0.sketch().segment((-18,-3),(-5,-3)).arc((0,-6),(5,-3)).segment((18,-3)).segment((18,3)).segment((5,3)).arc((0,6),(-5,3)).segment((-18,3)).close().assemble(),mode='s').finalize().extrude(-42)).union(w0.sketch().circle(20).circle(14,mode='s').finalize().extrude(8))
