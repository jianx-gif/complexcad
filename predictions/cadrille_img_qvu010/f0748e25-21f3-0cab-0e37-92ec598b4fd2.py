import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,14,0))
r=w0.sketch().segment((-91,-37),(-75,-37)).arc((-12,-74),(52,-37)).segment((68,-37)).segment((68,11)).segment((52,11)).arc((-12,48),(-75,11)).segment((-91,11)).close().assemble().finalize().extrude(198).union(w0.sketch().arc((-45,74),(-12,62),(16,43)).arc((30,64),(49,81)).arc((2,88),(-45,74)).assemble().finalize().extrude(200)).union(w1.sketch().arc((-99,-36),(-84,0),(-99,36)).segment((-99,28)).arc((-90,0),(-99,-28)).close().assemble().finalize().extrude(-99))