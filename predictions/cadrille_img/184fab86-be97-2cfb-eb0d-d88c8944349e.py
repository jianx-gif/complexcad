import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-49,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-38,-39),(-36,-37),(-34,-36)).arc((-36,-36),(-38,-35)).close().assemble().finalize().extrude(147).union(w1.sketch().arc((-100,-36),(15,41),(100,-71)).segment((100,-35)).arc((0,71),(-100,-35)).close().assemble().finalize().extrude(196))