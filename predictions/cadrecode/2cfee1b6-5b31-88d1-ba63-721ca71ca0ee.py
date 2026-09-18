import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('XY',origin=(0,0,44))
r=w0.workplane(offset=-50/2).cylinder(50,100).union(w0.sketch().circle(90).circle(26,mode='s').finalize().extrude(45)).union(w1.sketch().circle(100).circle(13,mode='s').finalize().extrude(-44))