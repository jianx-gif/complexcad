import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-36,0))
w1=cq.Workplane('YZ',origin=(-71,0,0))
r=w0.sketch().segment((-52,-48),(-50,-50)).segment((52,48)).segment((50,50)).close().assemble().finalize().extrude(119).union(w1.sketch().arc((-83,-58),(-55,-81),(-22,-95)).segment((-22,-100)).segment((22,-100)).segment((22,-95)).arc((55,-81),(83,-58)).segment((83,-57)).arc((55,0),(83,57)).segment((83,58)).segment((22,95)).segment((22,100)).segment((-22,100)).segment((-22,95)).arc((-55,81),(-83,58)).segment((-83,57)).arc((-55,0),(-83,-57)).close().assemble().finalize().extrude(171))