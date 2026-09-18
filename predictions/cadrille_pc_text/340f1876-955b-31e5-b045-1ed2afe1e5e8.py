import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
w1=cq.Workplane('XY',origin=(0,0,-25))
r=w0.sketch().circle(87).circle(63,mode='s').finalize().extrude(25).union(w1.sketch().rect(200,200).rect(8,132,mode='s').finalize().extrude(-12))