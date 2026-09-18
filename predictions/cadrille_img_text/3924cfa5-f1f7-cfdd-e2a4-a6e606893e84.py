import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-60,0))
w1=cq.Workplane('XY',origin=(0,0,71))
r=w0.sketch().arc((-89,-54),(-72,-67),(-54,-78)).segment((-54,-54)).close().assemble().reset().face(w0.sketch().segment((-89,54),(89,54)).arc((0,89),(-89,54)).assemble()).reset().face(w0.sketch().arc((54,-78),(72,-67),(89,-54)).segment((54,-54)).close().assemble()).finalize().extrude(160).union(w1.sketch().arc((-19,-60),(0,-62),(19,-60)).close().assemble().finalize().extrude(-142))