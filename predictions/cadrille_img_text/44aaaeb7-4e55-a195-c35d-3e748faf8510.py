import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,35,0))
r=w0.sketch().arc((-85,-49),(0,-78),(85,-49)).segment((74,-49)).arc((0,-76),(-74,-49)).close().assemble().reset().face(w0.sketch().segment((-85,49),(-74,49)).arc((0,76),(74,49)).segment((85,49)).arc((0,78),(-85,49)).assemble()).finalize().extrude(200).union(w1.sketch().push([(0,40)]).circle(25).circle(14,mode='s').finalize().extrude(-10))