import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-26,-100))
w1=cq.Workplane('XY',origin=(-100,-26,-100))
r=w0.sketch().circle(26).circle(25,mode='s').finalize().extrude(200).union(w1.sketch().rect(200,4).rect(2,4,mode='s').finalize().extrude(100))