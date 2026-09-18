import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('XY',origin=(0,0,60))
r=w0.workplane(offset=-5/2).box(100,100,5).union(w1.sketch().circle(40).circle(32,mode='s').finalize().extrude(-56))
