import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,97,0))
w1=cq.Workplane('ZX',origin=(0,39,0))
r=w0.sketch().segment((-59,-7),(-35,1)).arc((-25,23),(-4,35)).segment((10,58)).arc((-39,39),(-59,-7)).assemble().reset().face(w0.sketch().arc((-10,-58),(39,-39),(59,7)).segment((35,-1)).arc((25,-23),(4,-35)).close().assemble()).finalize().extrude(-194).union(w1.sketch().circle(100).circle(99,mode='s').finalize().extrude(-53))