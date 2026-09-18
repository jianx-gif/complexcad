import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,27))
r=w0.sketch().circle(78).push([(-66,-12)]).circle(3,mode='s').push([(-45,52)]).circle(4,mode='s').finalize().extrude(-54).union(w0.workplane(offset=-47/2).box(150,86,47)).union(w0.workplane(offset=-9/2).cylinder(9,100))