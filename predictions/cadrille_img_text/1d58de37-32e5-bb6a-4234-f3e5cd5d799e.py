import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-95))
w1=cq.Workplane('YZ',origin=(73,0,0))
r=w0.sketch().arc((-73,16),(-72,17),(-70,19)).arc((-71,20),(-72,21)).close().assemble().reset().face(w0.sketch().arc((-39,29),(18,48),(65,10)).arc((19,95),(-39,29)).assemble()).finalize().extrude(190).union(w1.sketch().arc((-50,-90),(-10,-6),(96,-19)).arc((-33,96),(-50,-90)).assemble().finalize().extrude(-133))