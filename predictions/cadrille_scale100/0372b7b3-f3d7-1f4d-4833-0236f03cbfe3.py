import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,25))
w1=cq.Workplane('XY',origin=(0,0,29))
r=w0.sketch().circle(20).rect(36,18,mode='s').finalize().extrude(-30).union(w0.sketch().circle(55).circle(50,mode='s').finalize().extrude(75)).union(w0.sketch().circle(49).circle(42,mode='s').finalize().extrude(75)).union(w1.workplane(offset=66/2).cylinder(66,50))