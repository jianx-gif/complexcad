import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-57))
w1=cq.Workplane('YZ',origin=(21,0,0))
r=w0.workplane(offset=20/2).cylinder(20,100).union(w0.sketch().circle(80).circle(40,mode='s').push([(64,29)]).circle(15,mode='s').finalize().extrude(120)).union(w1.sketch().push([(0,-24)]).circle(39).circle(17,mode='s').finalize().extrude(-44))