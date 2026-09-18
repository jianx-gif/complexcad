import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-36))
w1=cq.Workplane('XY',origin=(0,0,90))
r=w0.sketch().circle(36).circle(27,mode='s').finalize().extrude(-63).union(w0.sketch().circle(100).circle(90,mode='s').finalize().extrude(127)).union(w1.sketch().circle(82).circle(35,mode='s').finalize().extrude(9))