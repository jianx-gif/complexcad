import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-34,0))
w1=cq.Workplane('ZX',origin=(0,-93,0))
r=w0.workplane(offset=-7/2).cylinder(7,97).union(w0.sketch().arc((18,-79),(58,-61),(88,-30)).segment((100,-30)).segment((100,-1)).arc((-76,65),(18,-79)).assemble().finalize().extrude(94)).union(w1.sketch().arc((-100,19),(-97,17),(-95,15)).arc((94,-35),(-70,62)).arc((-89,58),(-100,43)).segment((-95,43)).arc((-97,31),(-97,19)).close().assemble().finalize().extrude(166))