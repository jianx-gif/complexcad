import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,67,0))
r=w0.sketch().rect(8,200).rect(8,4,mode='s').finalize().extrude(-134)