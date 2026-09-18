import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-58,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-92,-83),(-75,-79),(-59,-71)).segment((-59,-66)).segment((-51,-66)).arc((-34,-26),(-18,14)).close().assemble().reset().face(w0.sketch().arc((51,71),(75,67),(92,57)).segment((92,83)).segment((90,83)).segment((90,85)).segment((83,85)).segment((83,83)).segment((51,83)).close().assemble()).finalize().extrude(158).union(w1.sketch().arc((-34,-14),(1,-19),(34,-14)).arc((10,-3),(-7,17)).arc((-20,4),(-34,-10)).close().assemble().finalize().extrude(127))