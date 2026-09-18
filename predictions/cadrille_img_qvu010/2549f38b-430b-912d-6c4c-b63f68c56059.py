import cadquery as cq
w0=cq.Workplane('YZ',origin=(-53,0,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-84,21),(-78,-36),(-44,-83)).close().assemble().reset().face(w0.sketch().segment((-27,83),(-10,65)).segment((-10,67)).segment((10,67)).segment((10,39)).segment((84,-21)).arc((78,36),(44,83)).close().assemble()).finalize().extrude(112).union(w1.sketch().segment((-82,-27),(34,-27)).arc((-24,16),(-82,58)).close().assemble().finalize().extrude(-200))