import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-33))
r=w0.sketch().circle(100).circle(8,mode='s').push([(87,-12)]).rect(14,26,mode='s').finalize().extrude(66)