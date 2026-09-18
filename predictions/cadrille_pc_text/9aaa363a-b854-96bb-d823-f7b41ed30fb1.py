import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,2))
r=w0.sketch().rect(200,150).push([(-87,57)]).circle(2,mode='s').finalize().extrude(-20).union(w0.sketch().rect(180,130).circle(38,mode='s').finalize().extrude(16))