import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,17))
w1=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().circle(30).rect(36,30,mode='s').finalize().extrude(-17).union(w0.sketch().circle(27).circle(19,mode='s').finalize().extrude(13)).union(w1.workplane(offset=-30/2).cylinder(30,10))
