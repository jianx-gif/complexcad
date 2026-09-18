import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-30,0))
w1=cq.Workplane('XY',origin=(0,0,53))
r=w0.sketch().arc((-96,-4),(-94,-20),(-90,-36)).segment((96,-36)).segment((96,4)).segment((83,4)).arc((0,-35),(-83,4)).segment((-96,4)).close().assemble().reset().face(w0.sketch().segment((-96,48),(-83,48)).arc((0,97),(83,48)).segment((96,48)).segment((96,88)).segment((-96,88)).close().assemble()).finalize().extrude(120).union(w1.sketch().push([(0,-20)]).circle(80).circle(69,mode='s').finalize().extrude(-124))