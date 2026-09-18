import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,43))
w1=cq.Workplane('ZX',origin=(0,10,0))
r=w0.sketch().segment((-11,-9),(11,-9)).segment((11,9)).segment((-11,9)).segment((-11,7)).arc((-10,6),(-11,5)).close().assemble().finalize().extrude(-55).union(w0.sketch().segment((-11,-7),(11,-7)).segment((11,7)).segment((-11,7)).segment((-11,5)).arc((-10,4),(-11,3)).close().assemble().finalize().extrude(57)).union(w0.sketch().segment((-13,-3),(10,-6)).segment((11,3)).segment((-12,6)).close().assemble().rect(4,10,mode='s').finalize().extrude(57)).union(w1.sketch().arc((0,-20),(22,0),(0,20)).close().assemble().finalize().extrude(-20))
