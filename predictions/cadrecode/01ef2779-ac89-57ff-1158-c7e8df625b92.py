import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().rect(100,76).rect(76,50,mode='s').finalize().extrude(-200)