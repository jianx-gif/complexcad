import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,22,0))
w1=cq.Workplane('YZ',origin=(23,0,0))
r=w0.sketch().circle(25).circle(20,mode='s').finalize().extrude(-22).union(w0.sketch().circle(38).circle(25,mode='s').finalize().extrude(18)).union(w1.workplane(offset=-116/2).moveTo(0,20).cylinder(116,2))