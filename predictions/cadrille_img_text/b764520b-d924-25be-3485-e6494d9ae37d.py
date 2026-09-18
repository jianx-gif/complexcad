import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('XY',origin=(0,0,97))
r=w0.sketch().arc((-88,16),(-62,-21),(-22,-39)).segment((-22,-40)).segment((-19,-39)).arc((3,-35),(22,-25)).segment((25,-24)).segment((25,-23)).arc((63,21),(78,77)).arc((11,29),(-88,16)).assemble().finalize().extrude(-200).union(w1.sketch().arc((-48,-40),(15,-59),(78,-40)).segment((57,-40)).arc((15,-53),(-27,-40)).close().assemble().finalize().extrude(-145))