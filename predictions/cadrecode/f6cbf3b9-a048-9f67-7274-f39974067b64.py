import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('XY',origin=(0,0,-93))
r=w0.sketch().circle(79).reset().face(w0.sketch().segment((-63,-37),(-62,-37)).arc((-49,-53),(-29,-55)).arc((14,-71),(53,-48)).segment((54,-48)).segment((54,-47)).arc((71,-14),(62,22)).segment((63,37)).segment((62,37)).arc((49,53),(29,55)).arc((-40,57),(-62,-10)).close().assemble(),mode='s').finalize().extrude(200).union(w1.workplane(offset=-7/2).cylinder(7,72))