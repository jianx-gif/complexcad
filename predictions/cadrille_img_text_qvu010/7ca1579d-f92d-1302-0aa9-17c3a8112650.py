import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,24,0))
w1=cq.Workplane('ZX',origin=(0,71,0))
r=w0.sketch().segment((-100,48),(-13,12)).arc((-28,-31),(14,-50)).segment((14,-89)).segment((59,-48)).segment((-100,82)).close().assemble().finalize().extrude(-21).union(w1.sketch().arc((-59,89),(-11,1),(-58,90)).segment((-58,89)).close().assemble().finalize().extrude(-142))