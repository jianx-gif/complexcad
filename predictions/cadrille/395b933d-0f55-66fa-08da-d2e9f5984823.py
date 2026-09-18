import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-44))
w1=cq.Workplane('XY',origin=(0,0,-57))
r=w0.sketch().circle(100).circle(92,mode='s').finalize().extrude(100).union(w1.sketch().push([(-95,-50)]).rect(10,100).push([(95,50)]).rect(10,100).finalize().extrude(27))