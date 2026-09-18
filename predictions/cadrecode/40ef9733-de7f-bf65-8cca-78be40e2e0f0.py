import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,93,0))
w1=cq.Workplane('XY',origin=(0,0,-25))
r=w0.sketch().segment((-25,-8),(-8,-24)).segment((12,10)).segment((-10,24)).close().assemble().finalize().extrude(-191).union(w0.sketch().circle(52).circle(6,mode='s').finalize().extrude(-133)).union(w0.workplane(offset=5/2).cylinder(5,100)).union(w1.sketch().push([(0,26)]).circle(64).circle(49,mode='s').finalize().extrude(96))