import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
w1=cq.Workplane('ZX',origin=(0,-89,0))
r=w0.sketch().arc((-85,-46),(-14,-20),(85,-25)).arc((65,33),(26,82)).segment((26,98)).segment((-10,98)).arc((-44,67),(-85,46)).segment((-85,15)).arc((-77,-16),(-85,-46)).assemble().finalize().extrude(-200).union(w1.sketch().arc((-34,-100),(36,-1),(98,100)).segment((-34,100)).close().assemble().finalize().extrude(159))