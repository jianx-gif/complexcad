import cadquery as cq
w0=cq.Workplane('YZ',origin=(-49,0,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-33,-42),(-23,-56),(-10,-68)).segment((-10,89)).arc((-17,83),(-23,76)).segment((-23,-42)).close().assemble().reset().face(w0.sketch().arc((10,-68),(33,0),(10,68)).close().assemble()).finalize().extrude(135).union(w1.sketch().arc((-89,-58),(0,-82),(89,-58)).close().assemble().finalize().extrude(-200))