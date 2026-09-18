import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('YZ',origin=(75,0,0))
r=w0.sketch().arc((-49,-79),(-45,-82),(-41,-84)).segment((-41,-85)).segment((-39,-85)).arc((-37,-86),(-35,-87)).arc((-37,-85),(-39,-83)).arc((-44,-81),(-49,-79)).assemble().finalize().extrude(-200).union(w0.sketch().arc((-39,-87),(-37,-86),(-35,-85)).arc((-37,-85),(-39,-87)).assemble().finalize().extrude(-195)).union(w1.sketch().arc((-100,-53),(59,-73),(57,76)).segment((57,53)).arc((59,-50),(-53,-53)).close().assemble().finalize().extrude(-170))