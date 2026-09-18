import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,90,0))
r=w0.sketch().segment((-76,-59),(76,-59)).segment((76,59)).segment((-76,59)).segment((-76,-57)).arc((-73,-58),(-76,-59)).assemble().finalize().extrude(200).union(w1.sketch().push([(0,25)]).circle(75).circle(57,mode='s').finalize().extrude(-158))