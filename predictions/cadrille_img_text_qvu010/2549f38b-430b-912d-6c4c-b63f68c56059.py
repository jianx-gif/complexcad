import cadquery as cq
w0=cq.Workplane('YZ',origin=(-82,0,0))
w1=cq.Workplane('ZX',origin=(0,-28,0))
r=w0.sketch().segment((-50,100),(-12,65)).segment((-12,-73)).segment((-10,-73)).segment((-10,64)).segment((82,-27)).arc((26,39),(-50,100)).assemble().finalize().extrude(122).union(w1.sketch().arc((-100,-34),(-89,23),(-100,82)).close().assemble().finalize().extrude(67))