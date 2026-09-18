import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,57,0))
w1=cq.Workplane('ZX',origin=(0,19,0))
r=w0.sketch().segment((-59,55),(-43,40)).arc((-33,53),(-20,63)).segment((-20,100)).close().assemble().reset().face(w0.sketch().segment((20,-63),(59,-55)).segment((43,-40)).arc((33,-53),(20,-63)).assemble()).finalize().extrude(-114).union(w1.workplane(offset=-32/2).cylinder(32,83))