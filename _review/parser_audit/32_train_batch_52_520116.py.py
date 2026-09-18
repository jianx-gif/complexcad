import cadquery as cq
w0=cq.Workplane('YZ',origin=(-36,0,0))
w1=cq.Workplane('YZ',origin=(-51,0,0))
r=w0.sketch().segment((-72,-19),(-15,-41)).segment((17,43)).segment((-40,65)).close().assemble().finalize().extrude(-64).union(w1.workplane(offset=151/2).moveTo(21,-14).cylinder(151,51))