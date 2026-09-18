import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('ZX',origin=(0,96,0))
r=w0.sketch().arc((-79,45),(67,-74),(-27,93)).arc((-51,69),(-79,45)).assemble().finalize().extrude(-187).union(w1.sketch().push([(0,3)]).circle(97).circle(85,mode='s').finalize().extrude(-193))