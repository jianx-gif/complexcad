import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,10,0))
w1=cq.Workplane('YZ',origin=(-28,0,0))
r=w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(-29).union(w1.sketch().circle(99).circle(60,mode='s').finalize().extrude(57))