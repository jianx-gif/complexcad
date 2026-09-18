import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,84,0))
r=w0.sketch().circle(100).circle(89,mode='s').finalize().extrude(199).union(w1.sketch().arc((-61,-58),(-43,-16),(-61,27)).close().assemble().finalize().extrude(-149))