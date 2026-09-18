import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,60))
w1=cq.Workplane('XY',origin=(0,0,60))
r=w0.sketch().circle(40).circle(12,mode='s').finalize().extrude(-120).union(w0.sketch().circle(100).circle(56,mode='s').finalize().extrude(-59)).union(w1.sketch().circle(88).circle(12,mode='s').finalize().extrude(-63))