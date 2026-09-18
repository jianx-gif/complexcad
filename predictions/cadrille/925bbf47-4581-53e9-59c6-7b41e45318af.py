import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-4))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().rect(120,90).push([(-36,-19)]).circle(1,mode='s').push([(39,19)]).circle(1,mode='s').finalize().extrude(7).union(w0.workplane(offset=11/2).cylinder(11,29)).union(w1.workplane(offset=-200/2).moveTo(-4.5,2).box(7,4,200))