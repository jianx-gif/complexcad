import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,33))
r=w0.sketch().circle(100).circle(9,mode='s').push([(88,-11.5)]).rect(16,25,mode='s').finalize().extrude(-66)