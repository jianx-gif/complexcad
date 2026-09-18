import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,25))
r=w0.workplane(offset=-125/2).cylinder(125,2).union(w0.sketch().circle(20).circle(1,mode='s').finalize().extrude(-30)).union(w0.sketch().circle(55).circle(50,mode='s').finalize().extrude(75))
