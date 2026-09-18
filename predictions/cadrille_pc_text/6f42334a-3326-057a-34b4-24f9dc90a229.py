import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
w1=cq.Workplane('ZX',origin=(0,-33,0))
r=w0.sketch().segment((-32,-34),(-18,-43)).segment((38,-2)).segment((55,-1)).segment((54,16)).segment((47,15)).segment((50,18)).segment((36,18)).segment((36,15)).segment((28,12)).segment((28,13)).close().assemble().finalize().extrude(200).union(w1.sketch().arc((-55,-21),(1,-19),(55,1)).arc((47,19),(55,37)).arc((22,38),(-7,28)).arc((-2,10),(-16,22)).arc((-36,5),(-55,-21)).assemble().finalize().extrude(66))