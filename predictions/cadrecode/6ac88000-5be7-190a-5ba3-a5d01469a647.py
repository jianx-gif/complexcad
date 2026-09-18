import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-24))
w1=cq.Workplane('ZX',origin=(0,0,0))
r=w0.sketch().circle(80).circle(20,mode='s').finalize().extrude(-32).union(w0.sketch().circle(60).circle(20,mode='s').finalize().extrude(24)).union(w1.sketch().circle(100).circle(88,mode='s').finalize().extrude(16))