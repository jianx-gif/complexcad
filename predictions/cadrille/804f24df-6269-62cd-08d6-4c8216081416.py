import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,89,0))
w1=cq.Workplane('YZ',origin=(-42,0,0))
r=w0.sketch().segment((-30,-40),(-10,-60)).segment((11,-60)).segment((30,-40)).close().assemble().finalize().extrude(-179).union(w0.sketch().segment((-30,-40),(28,-40)).segment((28,43)).segment((-30,43)).segment((-30,3)).arc((-27,2),(-30,1)).close().assemble().finalize().extrude(-49)).union(w0.workplane(offset=11/2).moveTo(0,-4).cylinder(11,24)).union(w1.sketch().segment((-100,-30),(81,-30)).segment((81,-26)).arc((90,19),(44,23)).segment((-100,23)).close().assemble().finalize().extrude(42))