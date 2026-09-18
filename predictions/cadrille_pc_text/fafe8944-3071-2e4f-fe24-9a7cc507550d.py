import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,22))
r=w0.sketch().rect(200,120).rect(190,110,mode='s').finalize().extrude(-47).union(w0.workplane(offset=3/2).box(200,26,3))