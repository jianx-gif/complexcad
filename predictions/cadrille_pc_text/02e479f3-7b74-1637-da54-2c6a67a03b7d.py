import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-28))
w1=cq.Workplane('XY',origin=(0,0,-38))
r=w0.sketch().circle(83).circle(67,mode='s').finalize().extrude(-9).union(w0.workplane(offset=49/2).cylinder(49,67)).union(w1.sketch().circle(77).push([(-4,1)]).circle(64,mode='s').finalize().extrude(76))