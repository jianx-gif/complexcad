import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-11,0))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().arc((24,-60),(65,0),(24,60)).close().assemble().finalize().extrude(4).union(w1.sketch().arc((-10,-87),(-8,-86),(-7,-85)).arc((-10,85),(10,-85)).arc((11,-86),(11,-87)).arc((-10,87),(-10,-87)).assemble().finalize().extrude(-159))