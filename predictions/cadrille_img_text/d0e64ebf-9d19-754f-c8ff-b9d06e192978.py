import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('XY',origin=(0,0,88))
r=w0.sketch().segment((-74,-67),(-74,67)).arc((-92,0),(-74,-67)).assemble().reset().face(w0.sketch().arc((-60,-79),(0,-92),(60,-79)).close().assemble()).reset().face(w0.sketch().segment((-60,79),(60,79)).arc((0,92),(-60,79)).assemble()).reset().face(w0.sketch().arc((74,-67),(92,0),(74,67)).close().assemble()).finalize().extrude(-192).union(w1.sketch().push([(0,27)]).circle(59).circle(27,mode='s').finalize().extrude(-32))