import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,39,0))
w1=cq.Workplane('XY',origin=(0,0,61))
r=w0.sketch().arc((-39,-91),(-12,-15),(54,35)).arc((-51,33),(-39,-91)).assemble().finalize().extrude(-129).union(w1.sketch().arc((-88,10),(-18,-80),(88,-39)).segment((88,39)).arc((18,98),(-80,67)).arc((-66,35),(-88,10)).assemble().finalize().extrude(-109))