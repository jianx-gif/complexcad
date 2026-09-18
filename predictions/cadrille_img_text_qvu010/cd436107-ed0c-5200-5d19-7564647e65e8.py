import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,25,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-88,-53),(88,-53)).segment((88,46)).close().assemble().finalize().extrude(-112).union(w0.sketch().segment((-91,-46),(-31,-60)).segment((-31,-59)).segment((-91,-44)).close().assemble().finalize().extrude(42)).union(w1.sketch().arc((-99,-15),(-52,-1),(-19,37)).segment((-99,37)).close().assemble().finalize().extrude(-200))