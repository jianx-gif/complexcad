import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('ZX',origin=(0,-92,0))
r=w0.sketch().circle(100).circle(59,mode='s').finalize().extrude(-50).union(w1.sketch().arc((47,-77),(50,0),(47,77)).close().assemble().finalize().extrude(183))