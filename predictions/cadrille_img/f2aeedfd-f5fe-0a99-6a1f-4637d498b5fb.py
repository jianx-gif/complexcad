import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-16,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-99,-39),(-84,-39)).arc((-88,0),(-84,39)).segment((-99,39)).close().assemble().push([(57,46)]).circle(14).finalize().extrude(31).union(w1.sketch().arc((-78,-55),(0,-40),(78,-55)).segment((78,2)).arc((11,36),(-18,99)).arc((-49,81),(-78,55)).close().assemble().finalize().extrude(200))