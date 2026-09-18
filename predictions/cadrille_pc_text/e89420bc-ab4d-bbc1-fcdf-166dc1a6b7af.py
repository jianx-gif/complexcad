import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,9))
w1=cq.Workplane('ZX',origin=(0,51,0))
r=w0.sketch().segment((-84,28),(-70,-32)).segment((-56,-29)).arc((10,-75),(72,-24)).segment((86,-21)).segment((72,49)).segment((58,46)).arc((-10,74),(-62,29)).close().assemble().finalize().extrude(-7).union(w1.sketch().arc((-3,-100),(10,-86),(2,-68)).segment((2,99)).segment((-3,99)).segment((-3,-68)).arc((-10,-86),(-3,-100)).assemble().finalize().extrude(-101))