import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,38,0))
w1=cq.Workplane('ZX',origin=(0,59,0))
r=w0.sketch().segment((-61,-58),(-61,-57)).arc((0,-81),(61,-57)).segment((61,-58)).arc((81,0),(61,58)).segment((61,57)).arc((0,81),(-61,57)).segment((-61,58)).arc((-81,0),(-61,-58)).assemble().finalize().extrude(-67).union(w1.sketch().segment((-100,-1),(-83,-1)).arc((0,-83),(83,-1)).segment((100,-1)).segment((100,1)).segment((83,1)).arc((0,83),(-83,1)).segment((-100,1)).close().assemble().finalize().extrude(-117))