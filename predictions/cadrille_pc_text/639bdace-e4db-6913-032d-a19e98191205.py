import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,56,0))
r=w0.sketch().circle(67).reset().face(w0.sketch().segment((-17,-57),(17,-57)).segment((17,-1)).arc((18,0),(17,1)).segment((17,57)).segment((-17,57)).close().assemble(),mode='s').finalize().extrude(-112).union(w0.sketch().circle(100).circle(41,mode='s').finalize().extrude(-23))