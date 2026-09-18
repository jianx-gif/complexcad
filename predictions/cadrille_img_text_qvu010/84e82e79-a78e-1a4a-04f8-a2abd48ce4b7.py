import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-21,0))
r=w0.sketch().circle(100).circle(33,mode='s').finalize().extrude(19).union(w0.sketch().arc((-11,-19),(10,17),(-11,52)).close().assemble().finalize().extrude(42))