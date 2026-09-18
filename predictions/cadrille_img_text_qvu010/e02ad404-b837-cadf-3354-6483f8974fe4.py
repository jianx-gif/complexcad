import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,38,0))
w1=cq.Workplane('ZX',origin=(0,1,0))
r=w0.sketch().circle(100).circle(74,mode='s').finalize().extrude(-55).union(w1.sketch().arc((-12,-12),(0,-15),(12,-12)).close().assemble().finalize().extrude(-77))