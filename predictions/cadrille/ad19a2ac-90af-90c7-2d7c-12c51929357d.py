import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-59))
r=w0.sketch().circle(100).circle(67,mode='s').finalize().extrude(117).union(w0.sketch().circle(86).rect(132,14,mode='s').finalize().extrude(118))