import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,80))
r=w0.sketch().push([(0,-1)]).circle(79).circle(69,mode='s').finalize().extrude(-160).union(w0.workplane(offset=-20/2).cylinder(20,100))