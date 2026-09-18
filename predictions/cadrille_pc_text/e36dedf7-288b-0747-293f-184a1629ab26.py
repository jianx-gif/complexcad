import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-22))
w1=cq.Workplane('XY',origin=(0,0,20))
r=w0.sketch().circle(100).circle(83,mode='s').finalize().extrude(6).union(w0.sketch().circle(84).circle(77,mode='s').finalize().extrude(54)).union(w1.sketch().circle(84).rect(8,10,mode='s').finalize().extrude(-52))