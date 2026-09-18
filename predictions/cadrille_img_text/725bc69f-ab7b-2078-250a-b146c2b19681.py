import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,89,0))
w1=cq.Workplane('ZX',origin=(0,48,0))
r=w0.sketch().arc((-16,-48),(1,-4),(29,33)).segment((29,34)).segment((28,34)).arc((14,43),(-2,48)).close().assemble().finalize().extrude(-189).union(w0.sketch().arc((-4,-91),(1,-89),(5,-87)).arc((-1,-88),(-4,-91)).assemble().finalize().extrude(-179)).union(w1.sketch().arc((-39,-48),(18,-51),(67,-19)).arc((89,-1),(85,30)).arc((84,33),(83,36)).arc((-29,73),(-39,-48)).assemble().push([(21,16)]).circle(43,mode='s').finalize().extrude(-14))