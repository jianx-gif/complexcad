import cadquery as cq
w0=cq.Workplane('YZ',origin=(-95,0,0))
w1=cq.Workplane('ZX',origin=(0,-16,0))
r=w0.sketch().arc((-99,-25),(-74,-1),(-53,27)).segment((-53,87)).segment((-47,87)).segment((-47,91)).segment((-53,91)).segment((-53,92)).close().assemble().finalize().extrude(96).union(w0.sketch().arc((5,100),(13,79),(17,57)).segment((36,57)).segment((36,100)).close().assemble().finalize().extrude(191)).union(w1.sketch().segment((-100,-72),(-59,-72)).arc((-84,-2),(-100,72)).close().assemble().finalize().extrude(69))