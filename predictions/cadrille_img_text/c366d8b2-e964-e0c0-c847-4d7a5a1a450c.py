import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,-37,0))
r=w0.sketch().arc((-60,-59),(19,18),(29,-78)).segment((29,-49)).arc((44,-1),(29,47)).segment((29,59)).segment((18,59)).arc((-1,66),(-20,59)).segment((-60,59)).close().assemble().finalize().extrude(200).union(w1.sketch().arc((-99,-29),(-84,-19),(-68,-13)).arc((41,33),(10,-76)).arc((10,-83),(9,-90)).arc((45,61),(-99,-29)).assemble().finalize().extrude(105))