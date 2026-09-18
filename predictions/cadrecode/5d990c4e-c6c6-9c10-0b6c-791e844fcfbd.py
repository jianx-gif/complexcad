import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().circle(62).circle(50,mode='s').finalize().extrude(-200).union(w0.sketch().circle(67).circle(62,mode='s').finalize().extrude(-25))