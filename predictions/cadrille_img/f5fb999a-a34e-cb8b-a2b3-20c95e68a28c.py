import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-71,0))
w1=cq.Workplane('ZX',origin=(0,-69,0))
r=w0.sketch().circle(100).circle(57,mode='s').circle(18).finalize().extrude(109).union(w1.sketch().arc((-17,12),(14,18),(41,3)).arc((15,49),(-17,12)).assemble().finalize().extrude(139))