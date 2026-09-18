import cadquery as cq
w0=cq.Workplane('YZ',origin=(-64,0,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((-91,-47),(-81,-39),(-71,-32)).arc((-65,1),(-49,31)).arc((-50,44),(-53,56)).close().assemble().reset().face(w0.sketch().arc((49,47),(57,33),(63,17)).arc((68,13),(71,8)).arc((65,39),(49,67)).close().assemble()).finalize().extrude(101).union(w1.sketch().segment((-94,-10),(-29,-10)).arc((-65,16),(-94,49)).close().assemble().finalize().extrude(200))