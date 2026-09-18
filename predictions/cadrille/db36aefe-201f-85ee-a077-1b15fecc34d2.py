import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,39))
w1=cq.Workplane('YZ',origin=(-87,0,0))
r=w0.sketch().circle(96).circle(13,mode='s').finalize().extrude(-78).union(w0.sketch().circle(100).circle(26,mode='s').finalize().extrude(-37)).union(w1.sketch().circle(49).circle(14,mode='s').finalize().extrude(148))