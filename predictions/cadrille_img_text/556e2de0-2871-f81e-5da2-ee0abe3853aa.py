import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-89,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-35,-48),(100,0),(-35,48)).arc((-75,0),(-35,-48)).assemble().push([(34,-27)]).circle(53,mode='s').finalize().extrude(169).union(w1.sketch().arc((-55,-39),(1,-1),(55,39)).segment((-55,39)).close().assemble().finalize().extrude(43))