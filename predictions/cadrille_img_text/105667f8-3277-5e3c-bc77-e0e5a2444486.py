import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,9,0))
w1=cq.Workplane('YZ',origin=(99,0,0))
r=w0.sketch().segment((-100,-100),(-39,-100)).arc((-79,0),(-39,100)).segment((-100,100)).close().assemble().finalize().extrude(-49).union(w0.sketch().segment((-17,-29),(-15,-30)).segment((17,29)).segment((15,30)).close().assemble().finalize().extrude(81)).union(w1.sketch().arc((-89,-12),(-63,-1),(-35,5)).arc((-30,13),(-23,5)).arc((11,-1),(35,-19)).arc((-15,98),(-89,-12)).assemble().finalize().extrude(-176))