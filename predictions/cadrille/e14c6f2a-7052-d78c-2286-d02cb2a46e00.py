import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-78))
w1=cq.Workplane('XY',origin=(0,0,-95))
r=w0.sketch().segment((-66,-16),(-66,16)).arc((-67,0),(-66,-16)).assemble().finalize().extrude(167).union(w0.sketch().arc((-66,-12),(-56,-24),(-61,-37)).arc((61,10),(-66,-12)).assemble().finalize().extrude(167)).union(w1.sketch().segment((-67,-87),(-44,-87)).arc((0,-100),(44,-87)).segment((67,-87)).segment((67,-70)).arc((100,0),(67,70)).segment((67,87)).segment((44,87)).arc((0,100),(-44,87)).segment((-67,87)).segment((-67,70)).arc((-100,0),(-67,-70)).close().assemble().finalize().extrude(11))