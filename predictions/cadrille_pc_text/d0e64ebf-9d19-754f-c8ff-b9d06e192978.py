import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-75))
r=w0.sketch().circle(100).circle(38,mode='s').push([(29,73)]).circle(12,mode='s').finalize().extrude(150)