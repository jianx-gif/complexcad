import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-70))
w1=cq.Workplane('XY',origin=(0,0,-77))
r=w0.sketch().circle(100).circle(93,mode='s').finalize().extrude(140).union(w1.sketch().circle(88).circle(26,mode='s').finalize().extrude(147))