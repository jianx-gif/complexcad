import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-83))
w1=cq.Workplane('ZX',origin=(0,35,0))
r=w0.sketch().push([(-9,0)]).circle(91).circle(80,mode='s').finalize().extrude(183).union(w1.sketch().arc((-99,83),(-84,82),(-70,76)).arc((-70,91),(-68,100)).arc((-85,99),(-99,100)).arc((-100,92),(-99,83)).assemble().finalize().extrude(-69))