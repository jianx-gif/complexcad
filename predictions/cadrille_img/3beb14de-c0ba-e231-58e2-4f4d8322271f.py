import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-53,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-23,-21),(-15,-28)).segment((23,21)).segment((15,28)).close().assemble().finalize().extrude(10).union(w0.sketch().arc((55,78),(72,2),(74,-78)).arc((83,2),(55,78)).assemble().finalize().extrude(143)).union(w1.sketch().arc((-100,-82),(0,-74),(100,-82)).segment((100,82)).segment((-100,82)).close().assemble().finalize().extrude(159))