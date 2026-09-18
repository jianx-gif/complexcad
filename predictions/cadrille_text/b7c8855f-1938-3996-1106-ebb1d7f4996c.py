import cadquery as cq
w0=cq.Workplane('ZX',origin=(-100,100,0))
w1=cq.Workplane('ZX',origin=(-100,100,0))
r=w0.sketch().segment((-57,99),(-56,99)).segment((-56,100)).close().assemble().finalize().extrude(-200).union(w1.sketch().face(w1.sketch().segment((24,-4),(24,4)).arc((23,0),(24,-4)).assemble()).finalize().extrude(-200))