import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-8))
r=w0.sketch().rect(200,160).rect(160,120,mode='s').finalize().extrude(16)