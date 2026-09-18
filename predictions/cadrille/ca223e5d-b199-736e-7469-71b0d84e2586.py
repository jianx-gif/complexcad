import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().circle(86).circle(80,mode='s').finalize().extrude(-200).union(w0.sketch().circle(100).circle(80,mode='s').finalize().extrude(-80))