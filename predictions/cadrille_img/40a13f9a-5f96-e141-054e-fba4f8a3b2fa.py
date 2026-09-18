import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((-57,-39),(79,56),(-45,-53)).arc((-33,-57),(-21,-58)).arc((51,50),(-54,-25)).arc((-56,-32),(-57,-39)).assemble().finalize().extrude(-199).union(w0.sketch().arc((-73,-68),(69,73),(-62,-80)).segment((2,-80)).segment((2,-53)).arc((32,41),(-54,-10)).segment((-73,-10)).close().assemble().finalize().extrude(-169))