import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,10,0))
r=w0.workplane(offset=-70/2).moveTo(-1,0).cylinder(70,1).union(w0.sketch().circle(40).push([(18,0)]).circle(7,mode='s').finalize().extrude(35)).union(w0.workplane(offset=50/2).cylinder(50,29))
