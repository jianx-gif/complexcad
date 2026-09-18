import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-47))
w1=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().segment((-90,10),(-36,-35)).segment((90,20)).segment((36,35)).arc((-20,18),(-90,10)).assemble().finalize().extrude(96).union(w1.sketch().arc((18,-75),(20,-74),(21,-72)).segment((20,-72)).segment((20,72)).segment((21,72)).arc((20,74),(18,75)).close().assemble().finalize().extrude(200))