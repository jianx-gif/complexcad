import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().rect(200,100).circle(7,mode='s').finalize().extrude(-20)