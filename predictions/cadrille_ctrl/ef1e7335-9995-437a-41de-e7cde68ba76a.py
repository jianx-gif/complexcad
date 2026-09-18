import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.workplane(offset=6/2).box(80,60,6).union(w0.sketch().rect(30,60).circle(5,mode='s').finalize().extrude(18))
