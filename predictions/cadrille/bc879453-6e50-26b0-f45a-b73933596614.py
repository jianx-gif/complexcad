import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,27))
r=w0.sketch().circle(78).push([(-66,-12)]).circle(3,mode='s').push([(-46,52)]).circle(4,mode='s').push([(-21,-69)]).circle(5,mode='s').finalize().extrude(-54).union(w0.sketch().segment((52,-43),(52,59)).arc((-65,-37),(78,17)).segment((78,-43)).close().assemble().finalize().extrude(-47)).union(w0.workplane(offset=-9/2).cylinder(9,100))