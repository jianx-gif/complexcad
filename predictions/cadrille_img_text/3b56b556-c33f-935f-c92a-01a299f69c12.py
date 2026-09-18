import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-40,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-99,-43),(-96,-50)).segment((99,43)).segment((96,50)).close().assemble().finalize().extrude(120).union(w1.sketch().arc((-96,-59),(0,-100),(96,-59)).segment((77,-59)).arc((73,-61),(68,-63)).segment((68,-59)).segment((-68,-59)).segment((-68,-63)).arc((-73,-61),(-77,-59)).close().assemble().finalize().extrude(-200))