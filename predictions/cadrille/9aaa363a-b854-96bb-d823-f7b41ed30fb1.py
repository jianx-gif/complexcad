import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,3))
r=w0.sketch().rect(200,150).push([(-87,59)]).circle(2,mode='s').push([(0,0)]).rect(130,116,mode='s').finalize().extrude(-21).union(w0.sketch().rect(180,130).circle(38,mode='s').finalize().extrude(15))