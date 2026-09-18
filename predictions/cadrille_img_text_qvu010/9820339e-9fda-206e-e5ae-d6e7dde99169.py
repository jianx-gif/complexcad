import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-38,0))
w1=cq.Workplane('ZX',origin=(0,-97,0))
r=w0.sketch().arc((-99,-16),(0,-100),(99,-16)).segment((90,-16)).arc((0,-91),(-90,-16)).close().assemble().finalize().extrude(117).union(w1.sketch().segment((-100,-16),(-95,-16)).arc((0,-96),(95,-16)).segment((100,-16)).segment((100,16)).segment((95,16)).arc((0,96),(-95,16)).segment((-100,16)).close().assemble().push([(0,-1)]).circle(13,mode='s').finalize().extrude(163))