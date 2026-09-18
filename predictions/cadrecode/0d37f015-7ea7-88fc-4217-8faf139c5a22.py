import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-25))
w1=cq.Workplane('ZX',origin=(0,-45,0))
r=w0.sketch().circle(75).circle(54,mode='s').finalize().extrude(-24).union(w0.workplane(offset=125/2).cylinder(125,50)).union(w1.sketch().push([(-55,0)]).circle(45).circle(42,mode='s').finalize().extrude(89))