import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('XY',origin=(0,0,36))
r=w0.sketch().circle(40).circle(33,mode='s').finalize().extrude(21).union(w0.workplane(offset=60/2).cylinder(60,28)).union(w1.sketch().circle(36).push([(-31,-1)]).circle(3,mode='s').push([(0,0)]).circle(8,mode='s').push([(0,-31)]).rect(4,4,mode='s').finalize().extrude(-16))