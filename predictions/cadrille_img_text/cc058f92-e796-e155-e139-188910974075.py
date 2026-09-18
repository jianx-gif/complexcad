import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,52,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-89,-83),(-36,-83)).segment((-89,-52)).close().assemble().finalize().extrude(-58).union(w1.sketch().segment((-80,-52),(-69,-52)).arc((-46,-71),(-18,-83)).arc((-16,-77),(-13,-71)).arc((-58,-19),(-54,52)).segment((-80,52)).close().assemble().finalize().extrude(200))