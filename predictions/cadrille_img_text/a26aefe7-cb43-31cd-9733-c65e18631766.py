import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-34,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-17,12),(39,10),(94,-12)).arc((41,34),(-17,12)).assemble().finalize().extrude(124).union(w1.sketch().arc((-49,-38),(18,-30),(78,-55)).segment((78,-14)).segment((86,-14)).segment((86,14)).segment((78,14)).segment((78,20)).arc((18,34),(-41,14)).segment((-49,14)).close().assemble().finalize().extrude(-200))