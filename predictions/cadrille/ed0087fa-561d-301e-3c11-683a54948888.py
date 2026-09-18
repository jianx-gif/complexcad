import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,33))
w1=cq.Workplane('YZ',origin=(-78,0,0))
r=w0.sketch().circle(87).circle(48,mode='s').finalize().extrude(-66).union(w0.sketch().circle(100).circle(33,mode='s').finalize().extrude(-43)).union(w1.sketch().circle(34).circle(15,mode='s').finalize().extrude(160))