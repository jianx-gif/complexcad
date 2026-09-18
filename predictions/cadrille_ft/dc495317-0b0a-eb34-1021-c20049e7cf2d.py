import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,0,0))
r=w0.sketch().circle(38).circle(33,mode='s').finalize().extrude(-100).union(w0.sketch().arc((-25,0),(24,-5),(-24,7)).arc((-18,2),(-25,0)).assemble().circle(20,mode='s').finalize().extrude(100)).union(w0.workplane(offset=100/2).cylinder(100,11))