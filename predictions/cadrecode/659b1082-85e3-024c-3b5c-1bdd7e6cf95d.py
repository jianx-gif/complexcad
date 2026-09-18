import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-75))
r=w0.workplane(offset=124/2).cylinder(124,34).union(w0.sketch().circle(100).push([(-83,-43)]).circle(2,mode='s').push([(0,0)]).circle(80,mode='s').finalize().extrude(149)).union(w0.sketch().segment((-58,-33),(-46,-37)).segment((-46,-38)).segment((-43,-38)).segment((46,-68)).segment((58,-33)).close().assemble().finalize().extrude(151))