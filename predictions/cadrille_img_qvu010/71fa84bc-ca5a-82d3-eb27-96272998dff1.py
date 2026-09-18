import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-16,0))
w1=cq.Workplane('XY',origin=(0,0,-53))
r=w0.sketch().rect(200,196).circle(89,mode='s').circle(27).finalize().extrude(32).union(w1.sketch().arc((-10,-95),(10,0),(-10,95)).close().assemble().finalize().extrude(130))