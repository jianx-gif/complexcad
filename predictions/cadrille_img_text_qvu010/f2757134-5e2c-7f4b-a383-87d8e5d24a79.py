import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('XY',origin=(0,0,-97))
r=w0.sketch().segment((-99,-19),(-97,-19)).arc((-18,87),(61,-19)).segment((69,-19)).arc((-18,95),(-99,-19)).assemble().finalize().extrude(200).union(w1.sketch().arc((-10,-95),(3,-87),(14,-78)).segment((-10,-78)).close().assemble().finalize().extrude(162))