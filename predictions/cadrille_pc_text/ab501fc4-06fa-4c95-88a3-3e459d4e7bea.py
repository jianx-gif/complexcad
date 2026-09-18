import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,5))
w1=cq.Workplane('ZX',origin=(0,20,0))
r=w0.sketch().circle(79).push([(16,-66)]).circle(11,mode='s').finalize().extrude(-5).union(w0.workplane(offset=45/2).moveTo(1,0).cylinder(45,26)).union(w1.sketch().circle(100).circle(75,mode='s').finalize().extrude(-20))