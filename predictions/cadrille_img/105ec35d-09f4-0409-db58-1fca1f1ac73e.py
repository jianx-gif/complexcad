import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
w1=cq.Workplane('ZX',origin=(0,86,0))
r=w0.sketch().segment((-86,95),(-52,25)).arc((-49,32),(-45,38)).segment((-45,42)).segment((-42,42)).arc((-24,66),(-1,86)).arc((-44,94),(-86,95)).assemble().finalize().extrude(-182).union(w0.sketch().segment((-29,-95),(-10,-95)).segment((-10,-38)).arc((10,-38),(29,-33)).segment((-29,-33)).close().assemble().finalize().extrude(-133)).union(w1.sketch().arc((-19,-2),(16,-13),(51,-2)).segment((39,-2)).arc((16,-8),(-7,-2)).close().assemble().finalize().extrude(-109))