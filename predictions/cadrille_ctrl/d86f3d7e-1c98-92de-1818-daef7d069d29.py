import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,55))
w1=cq.Workplane('XY',origin=(0,0,60))
r=w0.sketch().circle(30).circle(25,mode='s').finalize().extrude(-55).union(w1.sketch().circle(32).circle(25,mode='s').finalize().extrude(-5))
