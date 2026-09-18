import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,64,0))
w1=cq.Workplane('YZ',origin=(76,0,0))
r=w0.sketch().segment((-1,-16),(90,36)).arc((-96,26),(81,-58)).segment((1,-10)).close().assemble().finalize().extrude(-163).union(w0.sketch().segment((-100,14),(-46,14)).segment((-46,-91)).arc((91,41),(-100,14)).assemble().finalize().extrude(-130)).union(w1.sketch().push([(12,0)]).circle(88).circle(83,mode='s').finalize().extrude(-142))