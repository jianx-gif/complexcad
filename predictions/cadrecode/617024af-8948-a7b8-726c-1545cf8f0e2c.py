import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-10))
r=w0.sketch().rect(200,140).rect(40,40,mode='s').finalize().extrude(20)