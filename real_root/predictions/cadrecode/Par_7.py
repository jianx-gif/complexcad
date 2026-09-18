import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-25))
w1=cq.Workplane('ZX',origin=(0,12,0))
r=w0.sketch().segment((-100,-25),(-88,-40)).segment((-63,-21)).arc((-77,-17),(-85,-5)).close().assemble().reset().face(w0.sketch().arc((-64,1),(-50,-3),(-42,-15)).segment((-18,4)).segment((-29,18)).close().assemble()).finalize().extrude(40).union(w1.sketch().arc((-21,-5),(1,-24),(25,-5)).segment((16,-5)).arc((0,100),(-16,-5)).close().assemble().push([(0,46)]).circle(31,mode='s').finalize().extrude(28))