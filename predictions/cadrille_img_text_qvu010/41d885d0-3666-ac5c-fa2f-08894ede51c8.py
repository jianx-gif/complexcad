import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,-75,0))
r=w0.sketch().segment((-94,1),(-3,1)).segment((-3,11)).segment((-94,11)).arc((-93,15),(-91,19)).arc((-25,85),(54,40)).arc((62,30),(68,18)).arc((-20,88),(-94,1)).assemble().finalize().extrude(200).union(w1.sketch().arc((-70,-54),(-14,-19),(43,-54)).segment((43,-36)).segment((-70,-36)).close().assemble().finalize().extrude(-12))