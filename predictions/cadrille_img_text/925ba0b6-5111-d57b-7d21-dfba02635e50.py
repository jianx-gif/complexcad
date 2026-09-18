import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-30,0))
w1=cq.Workplane('ZX',origin=(0,-67,0))
r=w0.sketch().segment((-36,53),(-34,53)).arc((0,75),(34,53)).segment((36,53)).arc((0,77),(-36,53)).assemble().finalize().extrude(97).union(w1.sketch().arc((-71,53),(19,21),(-65,-28)).arc((100,-10),(-36,83)).arc((-46,68),(-61,60)).arc((-66,57),(-71,53)).assemble().push([(23,27)]).circle(62,mode='s').finalize().extrude(123))