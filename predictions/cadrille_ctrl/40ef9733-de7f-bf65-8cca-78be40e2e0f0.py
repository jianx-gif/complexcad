import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,78,0))
r=w0.sketch().segment((-24,1),(2,0)).segment((2,4)).segment((-24,5)).close().assemble().finalize().extrude(-178).union(w0.workplane(offset=-59/2).cylinder(59,21)).union(w0.sketch().segment((-40,-5),(-39,-5)).arc((-31,-25),(-13,-37)).segment((-13,-38)).segment((13,-38)).segment((13,-37)).arc((31,-25),(39,-5)).segment((40,-5)).segment((40,5)).segment((39,5)).arc((31,25),(13,37)).segment((13,38)).segment((-13,38)).segment((-13,37)).arc((-31,25),(-39,5)).segment((-40,5)).close().assemble().finalize().extrude(2))
