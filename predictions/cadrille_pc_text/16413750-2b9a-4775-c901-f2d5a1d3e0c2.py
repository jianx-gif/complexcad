import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,67))
r=w0.sketch().circle(100).circle(90,mode='s').finalize().extrude(-167).union(w0.sketch().circle(93).circle(7,mode='s').finalize().extrude(33))