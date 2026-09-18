import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,12,0))
w1=cq.Workplane('ZX',origin=(0,10,0))
r=w0.sketch().segment((-30,-10),(-13,-20)).segment((-13,-19)).segment((-29,-19)).segment((-29,-10)).close().assemble().reset().face(w0.sketch().segment((-11,19),(5,19)).segment((5,9)).segment((18,9)).segment((18,0)).segment((24,10)).segment((-1,25)).close().assemble()).reset().face(w0.sketch().segment((-24,10),(-18,-1)).segment((11,14)).segment((6,25)).close().assemble()).finalize().extrude(-27).union(w0.sketch().segment((-6,2),(6,2)).arc((0,6),(-6,2)).assemble().finalize().extrude(15)).union(w1.sketch().push([(0,-1)]).circle(24).circle(13,mode='s').finalize().extrude(-25))
