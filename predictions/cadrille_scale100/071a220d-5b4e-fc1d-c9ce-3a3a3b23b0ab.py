import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,40))
w1=cq.Workplane('ZX',origin=(0,50,0))
r=w0.sketch().circle(50).rect(60,60,mode='s').finalize().extrude(-80).union(w1.workplane(offset=-100/2).box(90,14,100))