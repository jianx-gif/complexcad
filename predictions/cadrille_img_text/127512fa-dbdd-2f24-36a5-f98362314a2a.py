import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-38,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-12,1),(-10,1)).arc((-9,3),(-8,1)).segment((12,1)).arc((0,8),(-12,1)).assemble().finalize().extrude(132).union(w1.sketch().arc((-100,-35),(-1,-82),(100,-35)).segment((100,-29)).arc((96,-19),(93,-9)).segment((93,-29)).segment((-93,-29)).segment((-93,-9)).arc((-96,-19),(-100,-29)).close().assemble().finalize().extrude(-180))