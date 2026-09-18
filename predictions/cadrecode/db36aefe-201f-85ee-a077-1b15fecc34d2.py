import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,39))
w1=cq.Workplane('XY',origin=(0,0,37))
r=w0.sketch().circle(61).circle(13,mode='s').finalize().extrude(-78).union(w0.sketch().circle(98).rect(52,26,mode='s').finalize().extrude(-52)).union(w1.sketch().circle(51).circle(13,mode='s').finalize().extrude(-74))