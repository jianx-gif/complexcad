import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-94))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().circle(100).circle(88,mode='s').finalize().extrude(188).union(w0.workplane(offset=194/2).cylinder(194,68)).union(w1.sketch().circle(99).push([(58,31)]).circle(12,mode='s').finalize().extrude(194))