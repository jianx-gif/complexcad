import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,58,0))
r=w0.sketch().segment((-84,-58),(-84,-57)).segment((-8,-57)).arc((25,15),(-8,87)).segment((-84,87)).segment((-84,-43)).arc((-85,-51),(-84,-58)).assemble().finalize().extrude(200).union(w1.sketch().segment((-100,-19),(-84,-19)).arc((-94,3),(-100,27)).close().assemble().finalize().extrude(-129))