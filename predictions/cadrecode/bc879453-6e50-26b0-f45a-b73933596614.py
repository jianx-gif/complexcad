import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,18))
r=w0.sketch().circle(78).push([(-61,10)]).circle(4,mode='s').finalize().extrude(-45).union(w0.workplane(offset=-38/2).cylinder(38,78)).union(w0.workplane(offset=8/2).cylinder(8,100))