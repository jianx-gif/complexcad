import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-57,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-74,-19),(74,-10),(-74,19)).close().assemble().finalize().extrude(28).union(w0.sketch().arc((-49,-19),(-39,-36),(-35,-55)).arc((3,-45),(30,-19)).segment((30,19)).segment((49,19)).arc((-11,38),(-49,-19)).assemble().finalize().extrude(157)).union(w1.sketch().arc((-49,-1),(-41,-53),(7,-31)).arc((28,52),(-49,1)).close().assemble().finalize().extrude(103))