import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-70))
r=w0.workplane(offset=-5/2).cylinder(5,96).union(w0.sketch().circle(100).circle(95,mode='s').finalize().extrude(140)).union(w0.sketch().circle(54).circle(51,mode='s').finalize().extrude(145))