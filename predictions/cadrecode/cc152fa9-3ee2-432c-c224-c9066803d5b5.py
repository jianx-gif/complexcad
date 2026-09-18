import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('ZX',origin=(0,6,0))
r=w0.workplane(offset=13/2).cylinder(13,60).union(w0.sketch().circle(100).circle(65,mode='s').finalize().extrude(15)).union(w1.workplane(offset=-6/2).moveTo(0,0).box(50,40,6))