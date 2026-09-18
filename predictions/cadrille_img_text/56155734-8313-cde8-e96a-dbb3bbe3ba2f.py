import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-58,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((-55,-59),(14,1),(80,64)).arc((70,63),(60,63)).segment((60,59)).segment((55,59)).segment((55,63)).arc((-75,52),(-55,-59)).assemble().finalize().extrude(137).union(w1.sketch().arc((-75,-64),(-12,-29),(31,-87)).arc((14,86),(-75,-64)).assemble().finalize().extrude(200))