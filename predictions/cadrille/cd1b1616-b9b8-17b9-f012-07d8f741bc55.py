import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-50))
r=w0.workplane(offset=60/2).cylinder(60,39).union(w0.sketch().rect(200,200).rect(100,100,mode='s').finalize().extrude(100))