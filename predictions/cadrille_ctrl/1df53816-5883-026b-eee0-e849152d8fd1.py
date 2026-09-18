import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,18))
w1=cq.Workplane('XY',origin=(0,0,18))
r=w0.sketch().segment((-38,1),(-35,1)).segment((-35,10)).arc((-36,10),(-38,9)).close().assemble().reset().face(w0.sketch().segment((-33,14),(-24,14)).segment((-24,25)).segment((-33,25)).arc((-32,19),(-33,14)).assemble()).finalize().extrude(-18).union(w0.sketch().segment((-15,55),(27,0)).segment((38,7)).segment((4,64)).close().assemble().finalize().extrude(-18)).union(w0.sketch().segment((-15,-3),(15,-15)).segment((15,1)).segment((-11,1)).segment((-11,17)).close().assemble().finalize().extrude(-8)).union(w1.sketch().segment((-15,-1),(-14,-1)).segment((-14,0)).segment((-13,0)).segment((-13,-1)).segment((15,-1)).segment((15,1)).segment((-15,1)).close().assemble().finalize().extrude(-8))
