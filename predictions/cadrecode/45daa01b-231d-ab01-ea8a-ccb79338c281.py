import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,22))
w1=cq.Workplane('XY',origin=(0,0,-33))
r=w0.workplane(offset=11/2).cylinder(11,100).union(w1.sketch().circle(78).circle(34,mode='s').push([(65,5)]).circle(9,mode='s').finalize().extrude(37))