import cadquery as cq
w0=cq.Workplane('YZ',origin=(-40,0,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((-23,87),(-88,0),(-23,-87)).segment((-23,-59)).arc((-82,0),(-23,59)).close().assemble().reset().face(w0.sketch().arc((23,-87),(82,0),(23,87)).segment((23,59)).arc((82,0),(23,-59)).close().assemble()).finalize().extrude(130).union(w1.sketch().arc((-1,-60),(1,-59),(3,-59)).arc((-1,60),(1,-59)).close().assemble().finalize().extrude(-118))