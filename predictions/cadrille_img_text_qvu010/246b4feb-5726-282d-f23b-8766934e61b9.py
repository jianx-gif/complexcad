import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-27,0))
w1=cq.Workplane('ZX',origin=(0,-52,0))
r=w0.sketch().push([(0,-84)]).rect(200,20).circle(14,mode='s').finalize().extrude(54).union(w0.sketch().arc((-29,16),(28,-19),(-26,20)).arc((-26,17),(-29,16)).assemble().circle(22,mode='s').finalize().extrude(121)).union(w1.sketch().arc((-99,-1),(0,-80),(99,-1)).segment((39,-1)).arc((0,-39),(-39,-1)).close().assemble().finalize().extrude(-40))