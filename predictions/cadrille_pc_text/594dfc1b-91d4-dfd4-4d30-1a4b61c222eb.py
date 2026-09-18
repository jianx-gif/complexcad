import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-22))
w1=cq.Workplane('XY',origin=(0,0,-75))
r=w0.sketch().circle(95).circle(83,mode='s').finalize().extrude(-53).union(w0.workplane(offset=97/2).cylinder(97,70)).union(w1.sketch().circle(100).circle(82,mode='s').finalize().extrude(61))