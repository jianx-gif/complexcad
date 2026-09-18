import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-50,0))
w1=cq.Workplane('YZ',origin=(1,0,0))
r=w0.sketch().circle(87).circle(84,mode='s').finalize().extrude(100).union(w1.sketch().circle(100).circle(96,mode='s').finalize().extrude(-10))