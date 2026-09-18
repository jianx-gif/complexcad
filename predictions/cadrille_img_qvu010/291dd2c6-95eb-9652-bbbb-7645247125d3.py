import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-14,0))
w1=cq.Workplane('ZX',origin=(0,29,0))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-96,40),(-77,23)).arc((-55,-56),(27,-72)).segment((46,-89)).segment((96,-40)).segment((77,-23)).arc((55,56),(-27,72)).segment((-46,89)).close().assemble(),mode='s').finalize().extrude(34).union(w1.sketch().circle(81).circle(77,mode='s').finalize().extrude(-101))