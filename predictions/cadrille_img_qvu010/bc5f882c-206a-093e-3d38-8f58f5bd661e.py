import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-56,0))
w1=cq.Workplane('ZX',origin=(0,-99,0))
r=w0.sketch().arc((-99,-48),(-24,-1),(50,38)).arc((-51,71),(-99,-21)).close().assemble().finalize().extrude(145).union(w1.sketch().arc((-100,-1),(-95,-27),(-84,-51)).arc((-10,-29),(50,-80)).arc((76,-57),(93,-27)).arc((97,-23),(100,-19)).segment((100,-13)).arc((-1,39),(-100,-1)).assemble().finalize().extrude(197))