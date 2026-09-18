import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().rect(100,76).rect(76,50,mode='s').push([(47,35)]).circle(2,mode='s').finalize().extrude(200)