import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,50))
w1=cq.Workplane('XY',origin=(0,0,45))
r=w0.sketch().circle(40).circle(25,mode='s').finalize().extrude(-45).union(w0.sketch().circle(15).circle(8,mode='s').finalize().extrude(15)).union(w1.sketch().circle(15).circle(13,mode='s').finalize().extrude(-110))
