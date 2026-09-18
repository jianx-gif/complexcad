import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,57,0))
w1=cq.Workplane('ZX',origin=(0,38,0))
r=w0.sketch().arc((1,-2),(2,0),(1,2)).close().assemble().finalize().extrude(-115).union(w0.sketch().segment((-4,-85),(4,-85)).segment((4,-84)).arc((84,0),(4,84)).segment((4,85)).segment((-4,85)).segment((-4,84)).arc((-84,0),(-4,-84)).close().assemble().finalize().extrude(-115)).union(w1.sketch().arc((1,-5),(2,0),(1,5)).close().assemble().finalize().extrude(52))