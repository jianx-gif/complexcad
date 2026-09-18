import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().arc((-97,-29),(-35,-48),(20,-29)).close().assemble().reset().face(w0.sketch().arc((35,-29),(64,27),(35,84)).close().assemble()).finalize().extrude(-200).union(w0.sketch().arc((-89,48),(-14,-10),(71,-19)).arc((-13,-5),(-89,48)).assemble().finalize().extrude(-185))