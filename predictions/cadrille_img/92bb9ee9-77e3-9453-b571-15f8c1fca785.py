import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-29,0))
w1=cq.Workplane('ZX',origin=(0,-60,0))
r=w0.sketch().push([(10,11)]).circle(89).reset().face(w0.sketch().segment((-26,21),(-23,13)).segment((26,28)).segment((26,46)).close().assemble(),mode='s').reset().face(w0.sketch().segment((41,31),(67,41)).segment((63,50)).segment((41,42)).close().assemble(),mode='s').finalize().extrude(12).union(w0.sketch().segment((17,-53),(17,-49)).arc((-11,21),(48,69)).arc((-79,38),(17,-53)).assemble().finalize().extrude(97)).union(w1.workplane(offset=119/2).moveTo(10,11).cylinder(119,89))