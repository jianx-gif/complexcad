import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-12))
r=w0.sketch().rect(140,200).push([(-59,-10)]).circle(10,mode='s').finalize().extrude(16).union(w0.workplane(offset=24/2).box(80,28,24))