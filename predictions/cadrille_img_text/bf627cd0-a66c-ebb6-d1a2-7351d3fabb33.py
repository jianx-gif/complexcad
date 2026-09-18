import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-36,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-100,-4),(-5,-4)).segment((-5,-90)).arc((68,73),(-100,-4)).assemble().finalize().extrude(112).union(w1.sketch().push([(1,5)]).circle(95).circle(40,mode='s').finalize().extrude(199))