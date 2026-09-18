import cadquery as cq
w0=cq.Workplane('YZ',origin=(-8,0,0))
w1=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().rect(66,32).rect(60,26,mode='s').finalize().extrude(106).union(w1.workplane(offset=95/2).moveTo(0,3).box(40,16,95))