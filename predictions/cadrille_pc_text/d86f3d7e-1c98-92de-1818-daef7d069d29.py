import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,78))
r=w0.sketch().circle(94).circle(78,mode='s').finalize().extrude(-172).union(w0.sketch().circle(100).circle(78,mode='s').finalize().extrude(16))