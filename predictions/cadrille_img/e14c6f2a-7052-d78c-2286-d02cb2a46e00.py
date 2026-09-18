import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,96,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.workplane(offset=-193/2).moveTo(14,16).cylinder(193,64).union(w1.sketch().arc((-89,-44),(79,-28),(-20,98)).arc((-47,36),(-89,-12)).close().assemble().reset().face(w1.sketch().arc((-79,-46),(74,-27),(-20,96)).arc((21,-10),(-79,-46)).assemble(),mode='s').finalize().extrude(-185))