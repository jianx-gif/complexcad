import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,2))
w1=cq.Workplane('XY',origin=(0,0,7))
r=w0.workplane(offset=-7/2).cylinder(7,45).union(w0.sketch().segment((-27,14),(-26,10)).arc((-29,-7),(-20,-21)).segment((-19,-25)).segment((-15,-24)).arc((7,-28),(25,-15)).segment((27,-14)).segment((26,-10)).arc((29,7),(20,21)).segment((19,25)).segment((15,24)).arc((-7,28),(-25,15)).close().assemble().finalize().extrude(76)).union(w1.sketch().arc((-23,-19),(-12,-25),(-8,-37)).arc((18,33),(-23,-19)).assemble().finalize().extrude(71))
