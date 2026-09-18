import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-25,0))
w1=cq.Workplane('XY',origin=(0,0,-33))
r=w0.sketch().circle(100).circle(85,mode='s').finalize().extrude(25).union(w1.sketch().arc((-10,-25),(25,25),(-10,75)).segment((-10,67)).arc((13,25),(-10,-16)).close().assemble().finalize().extrude(67))