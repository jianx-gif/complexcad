import cadquery as cq
w0=cq.Workplane('XY').w1=cq.Workplane('XY',origin=(0,0,79))
r=w0.sketch().circle(94).circle(78,mode='s').finalize().extrude(-94).union(w0.sketch().circle(100).circle(79,mode='s').finalize().extrude(55)).union(w1.sketch().circle(94).circle(79,mode='s').finalize().extrude(-178))