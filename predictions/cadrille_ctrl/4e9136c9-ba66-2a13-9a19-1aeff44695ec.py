import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,20,0))
r=w0.sketch().segment((-40,5),(-22,5)).arc((18,5),(-19,-10)).segment((-39,-10)).arc((40,5),(-40,5)).assemble().finalize().extrude(-14).union(w0.sketch().segment((-39,-11),(-34,-21)).segment((-29,-19)).arc((14,-37),(37,4)).segment((42,6)).segment((37,16)).segment((32,14)).arc((-11,32),(-34,-8)).close().assemble().finalize().extrude(-14))
