import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-25,-14),(-21,-14)).segment((-21,-19)).segment((15,-19)).segment((-1,-14)).segment((25,-14)).segment((25,18)).segment((15,18)).segment((15,19)).segment((-21,19)).segment((-21,18)).segment((-25,18)).close().assemble().finalize().extrude(-200).union(w1.sketch().segment((-19,-25),(19,-25)).segment((19,25)).segment((-19,25)).segment((-19,-10)).arc((-14,-12),(-19,-13)).close().assemble().finalize().extrude(200))