import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-8))
w1=cq.Workplane('XY',origin=(0,0,-16))
r=w0.sketch().circle(100).circle(60,mode='s').finalize().extrude(-12).union(w1.sketch().circle(82).circle(80,mode='s').finalize().extrude(36))