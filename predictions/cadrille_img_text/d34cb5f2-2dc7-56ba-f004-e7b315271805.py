import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,95,0))
w1=cq.Workplane('XY',origin=(0,0,90))
r=w0.sketch().arc((-17,-22),(1,-12),(17,2)).close().assemble().reset().face(w0.sketch().segment((48,22),(52,17)).arc((50,20),(48,22)).assemble()).finalize().extrude(-191).union(w1.sketch().arc((63,-95),(68,-94),(73,-92)).segment((100,-92)).segment((100,-12)).arc((96,-19),(91,-25)).arc((88,-64),(63,-95)).assemble().finalize().extrude(-190))