import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,75,0))
w1=cq.Workplane('ZX',origin=(0,32,0))
r=w0.sketch().segment((-13,-100),(7,-100)).segment((7,-68)).segment((-8,-68)).segment((-8,-37)).segment((-1,-37)).segment((-1,-32)).segment((7,-32)).segment((7,42)).segment((-1,42)).segment((-1,47)).segment((7,47)).segment((7,100)).segment((-13,100)).close().assemble().push([(-6.5,0)]).rect(5,16,mode='s').push([(-4,0)]).rect(6,16,mode='s').finalize().extrude(-150).union(w1.sketch().segment((13,-48),(13,-46)).segment((15,-46)).arc((-14,-44),(15,-48)).close().assemble().finalize().extrude(-70))