import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,5))
w1=cq.Workplane('XY',origin=(0,0,20))
r=w0.sketch().circle(89).circle(88,mode='s').finalize().extrude(-12).union(w0.sketch().circle(100).circle(88,mode='s').finalize().extrude(20)).union(w1.sketch().circle(70).circle(50,mode='s').finalize().extrude(-45))