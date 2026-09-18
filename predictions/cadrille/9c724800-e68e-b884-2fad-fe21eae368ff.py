import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-2))
r=w0.sketch().rect(200,100).push([(39,-4)]).circle(19,mode='s').finalize().extrude(4)