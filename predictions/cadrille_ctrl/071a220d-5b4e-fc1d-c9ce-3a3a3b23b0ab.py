import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,40))
w1=cq.Workplane('YZ',origin=(-8,0,0))
r=w0.sketch().circle(50).rect(60,60,mode='s').finalize().extrude(-80).union(w1.workplane(offset=15/2).box(100,90,15))
