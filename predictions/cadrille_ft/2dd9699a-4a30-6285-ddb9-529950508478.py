import cadquery as cq
w0=cq.Workplane('XY').r flat_length).box(192,200,60).union(w0.sketch().rect(14,200).rect(12,12,mode='s').push([(74,10)]).circle(5,mode='s').finalize().extrude(-18))