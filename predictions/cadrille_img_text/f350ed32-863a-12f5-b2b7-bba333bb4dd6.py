import cadquery as cq
w0=cq.Workplane('YZ',origin=(-48,0,0))
w1=cq.Workplane('ZX',origin=(0,30,0))
r=w0.sketch().arc((-27,72),(22,33),(34,-29)).arc((61,-39),(87,-42)).arc((52,30),(-27,72)).assemble().finalize().extrude(124).union(w1.sketch().segment((-100,-97),(-95,-97)).arc((-19,10),(100,-80)).segment((100,97)).segment((-100,97)).close().assemble().finalize().extrude(-110))