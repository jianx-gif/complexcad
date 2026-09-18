import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,15,0))
w1=cq.Workplane('ZX',origin=(0,15,0))
r=w0.sketch().segment((-39,-13),(-37,-13)).arc((-1,-40),(36,-13)).segment((39,-13)).segment((39,13)).segment((36,13)).arc((-1,40),(-37,13)).segment((-39,13)).close().assemble().push([(-1,0)]).circle(32,mode='s').finalize().extrude(5).union(w1.sketch().arc((19,36),(20,34),(21,33)).arc((26,29),(29,24)).arc((29,25),(30,25)).arc((27,30),(22,33)).arc((21,33),(21,34)).arc((20,35),(19,36)).assemble().finalize().extrude(4))