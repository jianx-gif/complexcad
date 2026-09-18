import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-29,0))
w1=cq.Workplane('ZX',origin=(0,-39,0))
r=w0.sketch().segment((-100,5),(-85,5)).arc((99,-17),(-84,17)).segment((-100,17)).close().assemble().finalize().extrude(10).union(w0.sketch().arc((-13,-72),(1,-74),(15,-72)).close().assemble().reset().face(w0.sketch().segment((-13,72),(15,72)).arc((1,74),(-13,72)).assemble()).reset().face(w0.sketch().arc((16,-72),(54,0),(16,72)).segment((16,39)).arc((40,0),(16,-39)).close().assemble()).finalize().extrude(108)).union(w1.workplane(offset=79/2).moveTo(13,11).cylinder(79,87))