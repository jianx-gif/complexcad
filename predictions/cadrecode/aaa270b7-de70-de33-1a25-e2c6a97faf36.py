import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,35))
r=w0.sketch().circle(83).circle(12,mode='s').push([(40,0)]).circle(10,mode='s').finalize().extrude(-70).union(w0.workplane(offset=-7/2).cylinder(7,100))