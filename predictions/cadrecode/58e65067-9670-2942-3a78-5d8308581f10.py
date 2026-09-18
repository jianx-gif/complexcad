import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,66))
w1=cq.Workplane('XY',origin=(0,0,60))
r=w0.sketch().circle(100).circle(94,mode='s').finalize().extrude(-159).union(w0.workplane(offset=27/2).cylinder(27,31)).union(w1.workplane(offset=-147/2).cylinder(147,93))