import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('ZX',origin=(0,0,0))
r=w0.sketch().circle(79).push([(16,-67)]).circle(11,mode='s').finalize().extrude(5).union(w0.workplane(offset=50/2).moveTo(2,0).cylinder(50,26)).union(w1.sketch().circle(100).circle(75,mode='s').finalize().extrude(20))