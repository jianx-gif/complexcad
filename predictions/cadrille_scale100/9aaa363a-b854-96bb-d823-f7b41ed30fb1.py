import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-4))
r=w0.workplane(offset=-1/2).box(80,60,1).union(w0.sketch().rect(70,60).push([(10,18)]).circle(6,mode='s').finalize().extrude(8)).union(w0.sketch().rect(72,52).circle(15,mode='s').finalize().extrude(14))