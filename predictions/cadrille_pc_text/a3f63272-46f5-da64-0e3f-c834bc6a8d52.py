import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-8))
r=w0.sketch().circle(100).circle(69,mode='s').finalize().extrude(16)