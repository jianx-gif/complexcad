import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-29,0))
w1=cq.Workplane('ZX',origin=(0,-86,0))
r=w0.sketch().circle(57).circle(44,mode='s').finalize().extrude(40).union(w0.workplane(offset=115/2).cylinder(115,43)).union(w1.sketch().circle(100).push([(47,10)]).circle(7,mode='s').push([(85,12)]).circle(9,mode='s').finalize().extrude(57))