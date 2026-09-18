import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-75,0))
w1=cq.Workplane('YZ',origin=(-38,0,0))
r=w0.sketch().segment((-23,-100),(-3,-100)).segment((-3,-70)).arc((-12,-66),(-3,-62)).segment((-3,60)).arc((-12,64),(-3,68)).segment((-3,100)).segment((-23,100)).close().assemble().finalize().extrude(150).union(w1.workplane(offset=76/2).moveTo(0,-2).box(16,10,76))