import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-62,-1),(0,-62),(62,-1)).segment((50,-1)).arc((0,-50),(-50,-1)).close().assemble().reset().face(w0.sketch().segment((-62,1),(-50,1)).arc((0,50),(50,1)).segment((62,1)).arc((0,63),(-62,1)).assemble()).finalize().extrude(-200).union(w0.sketch().circle(67).circle(62,mode='s').finalize().extrude(-29))