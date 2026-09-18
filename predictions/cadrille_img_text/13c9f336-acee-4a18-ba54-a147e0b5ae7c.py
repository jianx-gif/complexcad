import cadquery as cq
w0=cq.Workplane('YZ',origin=(-75,0,0))
w1=cq.Workplane('XY',origin=(0,0,56))
r=w0.sketch().arc((-20,-85),(0,-87),(20,-85)).close().assemble().reset().face(w0.sketch().segment((-20,85),(20,85)).arc((0,87),(-20,85)).assemble()).finalize().extrude(175).union(w1.sketch().arc((1,-87),(40,0),(1,87)).close().assemble().finalize().extrude(-156))