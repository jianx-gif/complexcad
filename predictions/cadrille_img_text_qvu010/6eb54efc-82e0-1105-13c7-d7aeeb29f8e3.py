import cadquery as cq
w0=cq.Workplane('YZ',origin=(-38,0,0))
w1=cq.Workplane('ZX',origin=(0,-19,0))
r=w0.sketch().arc((-86,-46),(-70,-31),(-53,-20)).arc((-48,-16),(-42,-16)).arc((-19,-19),(2,-30)).arc((4,-33),(6,-36)).arc((10,-41),(13,-46)).arc((48,19),(42,96)).arc((35,87),(27,79)).arc((29,21),(-23,-4)).arc((-27,-10),(-33,-13)).arc((-59,-26),(-86,-46)).assemble().finalize().extrude(106).union(w1.sketch().arc((-100,-59),(-70,-1),(-100,57)).close().assemble().finalize().extrude(-71))