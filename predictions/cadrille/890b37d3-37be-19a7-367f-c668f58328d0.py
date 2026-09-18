import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-80,0))
r=w0.sketch().segment((-4,-100),(4,-100)).segment((4,-62)).arc((0,-61),(4,-59)).segment((4,100)).segment((-4,100)).close().assemble().push([(0,22)]).circle(4,mode='s').finalize().extrude(160)