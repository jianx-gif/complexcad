import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('XY',origin=(0,0,99))
r=w0.sketch().circle(67).circle(50,mode='s').finalize().extrude(-200).union(w1.sketch().circle(98).circle(71,mode='s').finalize().extrude(-51))