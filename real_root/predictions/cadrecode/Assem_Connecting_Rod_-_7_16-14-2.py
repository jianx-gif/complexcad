import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-61,0))
w1=cq.Workplane('ZX',origin=(0,-86,0))
r=w0.sketch().circle(24).circle(12,mode='s').finalize().extrude(-39).union(w0.workplane(offset=-15/2).cylinder(15,32)).union(w0.workplane(offset=139/2).cylinder(139,20)).union(w1.workplane(offset=186/2).cylinder(186,19))