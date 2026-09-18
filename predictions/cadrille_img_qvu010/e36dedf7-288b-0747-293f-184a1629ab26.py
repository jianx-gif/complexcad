import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-31,0))
w1=cq.Workplane('ZX',origin=(0,14,0))
r=w0.sketch().circle(90).circle(83,mode='s').finalize().extrude(-4).union(w0.sketch().circle(100).reset().face(w0.sketch().segment((-21,-11),(-17,-19)).segment((21,11)).segment((17,19)).close().assemble(),mode='s').finalize().extrude(88)).union(w1.sketch().circle(92).circle(81,mode='s').finalize().extrude(-48))