import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,34,0))
w1=cq.Workplane('ZX',origin=(0,69,0))
r=w0.sketch().arc((-100,20),(0,-100),(100,20)).segment((93,20)).arc((0,-93),(-93,20)).close().assemble().push([(0,11)]).circle(29).finalize().extrude(-48).union(w1.sketch().arc((-3,-1),(0,-3),(3,-1)).close().assemble().finalize().extrude(-137))