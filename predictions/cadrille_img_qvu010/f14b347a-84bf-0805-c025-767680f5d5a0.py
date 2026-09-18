import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
w1=cq.Workplane('ZX',origin=(0,-6,0))
r=w0.sketch().arc((-92,-16),(-69,-23),(-45,-28)).arc((-67,-11),(-92,5)).close().assemble().finalize().extrude(27).union(w0.sketch().segment((12,7),(54,22)).arc((32,17),(12,7)).assemble().finalize().extrude(200)).union(w1.sketch().segment((-49,-100),(86,-100)).segment((86,-94)).arc((67,-97),(49,-97)).arc((44,-99),(39,-96)).arc((-10,-83),(-49,-51)).segment((-49,-96)).arc((-47,-97),(-49,-99)).close().assemble().finalize().extrude(50))