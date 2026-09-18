import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.workplane(offset=-84/2).cylinder(84,2).union(w0.sketch().circle(29).circle(20,mode='s').finalize().extrude(80)).union(w0.sketch().circle(34).circle(30,mode='s').circle(22).finalize().extrude(83))