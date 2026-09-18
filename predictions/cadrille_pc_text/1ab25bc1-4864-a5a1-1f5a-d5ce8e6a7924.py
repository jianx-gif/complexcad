import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-70))
w1=cq.Workplane('XY',origin=(0,0,-30))
r=w0.sketch().circle(100).circle(95,mode='s').finalize().extrude(140).union(w1.sketch().circle(35).circle(29,mode='s').finalize().extrude(130))