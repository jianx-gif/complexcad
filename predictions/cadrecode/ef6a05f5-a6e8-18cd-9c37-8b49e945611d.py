import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-47,0))
w1=cq.Workplane('XY',origin=(0,0,-36))
r=w0.sketch().segment((-61,-76),(-50,-100)).segment((65,-36)).segment((54,-12)).segment((27,-24)).arc((-29,59),(-18,-42)).close().assemble().finalize().extrude(70).union(w0.sketch().segment((67,-27),(67,98)).arc((-1,35),(67,-27)).assemble().push([(39,5)]).circle(16,mode='s').finalize().extrude(74)).union(w0.workplane(offset=89/2).moveTo(-5,-26).cylinder(89,49)).union(w1.workplane(offset=73/2).moveTo(-26,26).cylinder(73,20))