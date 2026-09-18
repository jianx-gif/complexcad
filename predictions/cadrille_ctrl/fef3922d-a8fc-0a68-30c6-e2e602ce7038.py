import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.workplane(offset=-2/2).cylinder(2,5).union(w0.sketch().segment((-20,-3),(-18,-3)).arc((0,-20),(18,-3)).segment((20,-3)).segment((20,3)).segment((18,3)).arc((0,20),(-18,3)).segment((-20,3)).close().assemble().finalize().extrude(10)).union(w0.sketch().arc((-14,-2),(14,-4),(-13,5)).arc((-16,2),(-14,-2)).assemble().finalize().extrude(80))
