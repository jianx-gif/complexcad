import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-57,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-97,20),(-67,43)).arc((-84,34),(-97,20)).assemble().reset().face(w0.sketch().segment((-54,43),(54,-49)).arc((33,36),(-54,43)).assemble()).finalize().extrude(135).union(w1.sketch().circle(100).reset().face(w1.sketch().segment((-15,-35),(15,-35)).segment((15,35)).segment((-15,35)).segment((-15,33)).arc((-12,31),(-15,29)).close().assemble(),mode='s').finalize().extrude(149))