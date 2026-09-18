import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-97,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-96,-40),(0,-90),(96,-40)).segment((95,-40)).arc((0,-88),(-95,-40)).close().assemble().reset().face(w0.sketch().segment((-96,40),(-95,40)).arc((0,88),(95,40)).segment((96,40)).arc((0,90),(-96,40)).assemble()).finalize().extrude(197).union(w1.sketch().circle(90).circle(57,mode='s').finalize().extrude(197))