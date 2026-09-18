import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,6))
w1=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().circle(50).circle(30,mode='s').finalize().extrude(-6).union(w0.sketch().circle(41).circle(40,mode='s').finalize().extrude(14)).union(w1.sketch().circle(30).circle(30,mode='s').finalize().extrude(10))