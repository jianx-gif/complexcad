import cadquery as cq
w0=cq.Workplane('YZ',origin=(-77,0,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-78,-46),(-78,-44)).arc((-79,-45),(-78,-46)).assemble().finalize().extrude(155).union(w1.sketch().arc((-100,-71),(35,23),(100,-80)).segment((100,63)).arc((97,66),(100,69)).segment((100,71)).segment((89,71)).arc((0,2),(-89,71)).segment((-100,71)).close().assemble().finalize().extrude(182))