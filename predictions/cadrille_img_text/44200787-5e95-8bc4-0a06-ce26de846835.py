import cadquery as cq
w0=cq.Workplane('YZ',origin=(-67,0,0))
w1=cq.Workplane('ZX',origin=(0,-78,0))
r=w0.sketch().arc((-80,83),(-69,68),(-62,51)).arc((-55,48),(-49,44)).arc((-47,43),(-45,42)).arc((-54,69),(-80,83)).assemble().finalize().extrude(167).union(w1.sketch().arc((-100,-67),(-87,-59),(-74,-53)).arc((-26,12),(53,33)).segment((53,67)).segment((-53,67)).segment((-53,33)).arc((-67,29),(-80,22)).arc((-87,28),(-100,33)).close().assemble().finalize().extrude(136))