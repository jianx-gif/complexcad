import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-14,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-99,-18),(-65,-18)).arc((-84,32),(-65,82)).segment((-99,82)).close().assemble().finalize().extrude(-35).union(w1.sketch().segment((-82,-59),(-81,-59)).arc((-69,-46),(-55,-36)).arc((-55,-26),(-53,-16)).arc((-52,-10),(-49,-5)).arc((-22,33),(23,43)).arc((34,57),(46,69)).segment((46,70)).segment((-81,70)).segment((-82,70)).segment((-82,-16)).arc((-83,-24),(-82,-32)).close().assemble().finalize().extrude(-194))