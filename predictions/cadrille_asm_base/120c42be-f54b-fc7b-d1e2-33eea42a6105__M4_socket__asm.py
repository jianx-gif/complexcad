import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-18))
w1=cq.Workplane('XY',origin=(0,0,-4))
r=w0.sketch().segment((-60,-39),(-43,-39)).arc((-52,-33),(-60,-26)).close().assemble().finalize().extrude(38).union(w0.workplane(offset=35/2).cylinder(35,10)).union(w1.sketch().segment((-100,-62),(100,-62)).segment((100,62)).segment((-100,62)).segment((-100,59)).segment((-99,59)).segment((-99,57)).segment((-100,57)).close().assemble().finalize().extrude(12))