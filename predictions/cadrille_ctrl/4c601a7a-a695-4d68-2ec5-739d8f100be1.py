import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,5))
r=w0.sketch().segment((-45,-15),(-31,-15)).arc((-38,-1),(-31,15)).segment((-45,15)).close().assemble().reset().face(w0.sketch().segment((31,-15),(45,-15)).segment((45,15)).segment((31,15)).arc((38,1),(31,-15)).assemble()).finalize().extrude(-5).union(w0.sketch().segment((-2,-15),(2,-15)).segment((2,15)).segment((-2,15)).segment((-2,14)).arc((0,12),(-2,11)).close().assemble().finalize().extrude(-5))
