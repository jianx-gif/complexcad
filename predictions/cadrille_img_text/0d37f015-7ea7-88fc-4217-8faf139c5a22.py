import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('ZX',origin=(0,38,0))
r=w0.sketch().arc((-38,35),(-29,43),(-19,50)).segment((-38,50)).close().assemble().finalize().extrude(-199).union(w0.sketch().segment((-18,-86),(18,-86)).segment((18,-50)).arc((52,0),(18,50)).segment((18,86)).segment((-18,86)).segment((-18,50)).arc((-52,0),(-18,-50)).close().assemble().circle(49,mode='s').finalize().extrude(-19)).union(w1.sketch().arc((-67,-46),(64,-33),(33,86)).arc((31,83),(30,86)).arc((-11,81),(-46,59)).arc((-44,5),(-67,-46)).assemble().finalize().extrude(-22))