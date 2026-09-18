import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,0,0))
w1=cq.Workplane('ZX',origin=(0,40,0))
r=w0.sketch().arc((-27,14),(26,-16),(-24,19)).segment((-22,19)).segment((-22,14)).close().assemble().reset().face(w0.sketch().segment((-18,-16),(-8,-16)).segment((-8,-22)).segment((8,-22)).segment((8,-16)).segment((18,-16)).segment((18,13)).segment((8,13)).segment((8,22)).segment((-8,22)).segment((-8,13)).segment((-18,13)).close().assemble(),mode='s').finalize().extrude(10).union(w0.sketch().arc((-8,-13),(0,-15),(8,-13)).close().assemble().reset().face(w0.sketch().segment((-8,13),(8,13)).arc((0,15),(-8,13)).assemble()).finalize().extrude(29)).union(w1.workplane(offset=10/2).cylinder(10,45))
