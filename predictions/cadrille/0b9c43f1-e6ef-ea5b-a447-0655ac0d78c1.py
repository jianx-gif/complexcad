import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,95,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((-51,-23),(49,-2),(-48,-30)).segment((-44,-30)).arc((47,-2),(-46,22)).segment((-51,22)).close().assemble().finalize().extrude(-190).union(w1.sketch().arc((-10,78),(-78,-26),(39,-75)).segment((39,-66)).segment((53,-66)).arc((81,20),(16,79)).arc((2,86),(-10,78)).assemble().finalize().extrude(-5))