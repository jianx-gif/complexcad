import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-36,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-100,58),(-67,58)).arc((-84,78),(-100,100)).close().assemble().finalize().extrude(125).union(w1.sketch().arc((-98,-83),(0,-70),(98,-83)).segment((98,83)).segment((-98,83)).close().assemble().push([(29,33)]).circle(23,mode='s').finalize().extrude(119))