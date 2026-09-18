import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-8))
r=w0.sketch().rect(166,112).push([(-47,36)]).circle(4,mode='s').push([(33,44)]).circle(9,mode='s').finalize().extrude(10).union(w0.sketch().rect(200,160).rect(160,128,mode='s').finalize().extrude(16))