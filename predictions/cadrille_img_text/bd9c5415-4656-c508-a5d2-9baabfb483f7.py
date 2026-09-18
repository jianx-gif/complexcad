import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-80,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-86,-62),(86,-54)).segment((86,-49)).segment((-86,-57)).close().assemble().finalize().extrude(160).union(w1.sketch().segment((-99,-100),(99,-100)).segment((99,100)).segment((97,100)).arc((0,-86),(-97,100)).segment((-99,100)).close().assemble().finalize().extrude(200))