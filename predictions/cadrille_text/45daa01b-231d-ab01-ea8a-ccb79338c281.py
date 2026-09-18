import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-10))
w1=cq.Workplane('XY',origin=(-100,-50,-10))
r=w0.sketch().circle(50).circle(30,mode='s').finalize().extrude(150).union(w1.sketch().rect(200,10).rect(4,6,mode='s').finalize().extrude(-10))