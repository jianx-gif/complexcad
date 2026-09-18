import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('XY',origin=(0,0,-14))
r=w0.sketch().circle(63).circle(52,mode='s').finalize().extrude(-177).union(w0.sketch().circle(86).circle(11,mode='s').finalize().extrude(-14)).union(w1.sketch().circle(86).circle(51,mode='s').finalize().extrude(-86))