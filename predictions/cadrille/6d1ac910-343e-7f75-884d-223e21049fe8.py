import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,71,0))
r=w0.sketch().segment((-4,-92),(4,-92)).segment((4,100)).segment((-4,98)).close().assemble().push([(0,11)]).circle(3,mode='s').finalize().extrude(-141).union(w0.sketch().arc((-1,-100),(4,-41),(-1,18)).close().assemble().finalize().extrude(-39))