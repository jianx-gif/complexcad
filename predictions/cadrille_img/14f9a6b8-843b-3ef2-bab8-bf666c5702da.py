import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-59,0))
w1=cq.Workplane('YZ',origin=(46,0,0))
r=w0.sketch().arc((-89,9),(-65,-43),(-19,-77)).segment((-19,-80)).segment((-11,-80)).arc((43,-86),(89,-99)).close().assemble().finalize().extrude(149).union(w1.sketch().arc((-92,-53),(-26,-29),(30,15)).segment((30,20)).segment((35,20)).arc((64,43),(92,64)).arc((-19,61),(-92,-53)).assemble().finalize().extrude(-146))