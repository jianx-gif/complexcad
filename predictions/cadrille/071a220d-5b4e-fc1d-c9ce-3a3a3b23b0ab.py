import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-80))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().circle(99).rect(122,120,mode='s').finalize().extrude(160).union(w1.sketch().rect(180,30).rect(24,28,mode='s').finalize().extrude(-200))