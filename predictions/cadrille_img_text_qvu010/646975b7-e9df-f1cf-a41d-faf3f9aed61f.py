import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-67,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-35,-83),(35,-83)).segment((35,-53)).arc((0,-64),(-35,-53)).close().assemble().finalize().extrude(167).union(w1.sketch().segment((-100,-100),(100,-100)).arc((0,100),(-100,-100)).assemble().circle(94,mode='s').finalize().extrude(199))