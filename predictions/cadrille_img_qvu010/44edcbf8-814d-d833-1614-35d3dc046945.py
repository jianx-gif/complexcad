import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-97,0))
w1=cq.Workplane('ZX',origin=(0,-60,0))
r=w0.sketch().circle(81).circle(79,mode='s').finalize().extrude(194).union(w1.sketch().segment((-100,-44),(-97,-44)).arc((-35,-96),(43,-78)).arc((58,-67),(69,-53)).arc((84,-35),(94,-13)).segment((100,-13)).segment((100,44)).segment((94,44)).arc((40,95),(-32,89)).arc((-34,86),(-37,86)).arc((-73,63),(-94,26)).segment((-100,26)).close().assemble().circle(96,mode='s').finalize().extrude(120))