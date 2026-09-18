import cadquery as cq
w0=cq.Workplane('YZ',origin=(-79,0,0))
w1=cq.Workplane('ZX',origin=(0,-46,0))
r=w0.sketch().arc((-99,-19),(-77,-1),(-54,15)).arc((-52,22),(-48,28)).arc((-45,62),(-35,94)).arc((-85,49),(-99,-19)).assemble().finalize().extrude(84).union(w0.sketch().arc((6,100),(13,79),(17,58)).segment((36,58)).segment((36,100)).close().assemble().finalize().extrude(179)).union(w1.sketch().segment((-100,-72),(-48,-72)).arc((-79,-1),(-48,94)).segment((-100,94)).close().assemble().finalize().extrude(95))