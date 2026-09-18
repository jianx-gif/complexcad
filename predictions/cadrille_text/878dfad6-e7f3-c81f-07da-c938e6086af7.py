import cadquery as cq
w0=cq.Workplane('XY',origin=(-80,-100,-83))
r=w0.sketch().segment((-86,100),(-85,97)).segment((-85,100)).close().assemble().reset().face(w0.sketch().segment((-84,80),(-83,80)).segment((-83,82)).close().assemble()).reset().face(w0.sketch().segment((83,-80),(84,-80)).segment((84,-82)).segment((84,-84)).close().assemble()).finalize().extrude(167)