import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,24))
r=w0.sketch().circle(35).push([(-31,-3)]).circle(2,mode='s').finalize().extrude(-24).union(w0.sketch().circle(35).circle(29,mode='s').finalize().extrude(-23)).union(w0.workplane(offset=-4/2).cylinder(4,45))
