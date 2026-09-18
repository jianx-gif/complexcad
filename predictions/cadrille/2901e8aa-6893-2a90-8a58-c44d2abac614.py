import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().circle(20).circle(13,mode='s').finalize().extrude(-200).union(w0.sketch().circle(33).circle(21,mode='s').finalize().extrude(-12))