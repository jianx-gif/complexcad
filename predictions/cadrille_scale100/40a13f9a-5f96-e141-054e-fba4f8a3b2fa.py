import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,42))
r=w0.sketch().arc((13,-2),(14,0),(13,2)).close().assemble().finalize().extrude(-92).union(w0.sketch().circle(30).reset().face(w0.sketch().segment((-20,1),(-17,-4)).segment((20,-1)).segment((17,4)).close().assemble(),mode='s').finalize().extrude(-42)).union(w0.sketch().circle(20).circle(14,mode='s').finalize().extrude(8))