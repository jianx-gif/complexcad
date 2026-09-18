import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,23))
r=w0.sketch().circle(100).circle(91,mode='s').finalize().extrude(-55).union(w0.sketch().circle(91).circle(34,mode='s').finalize().extrude(9))