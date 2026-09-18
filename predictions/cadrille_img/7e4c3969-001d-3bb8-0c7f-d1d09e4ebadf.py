import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-1,0))
w1=cq.Workplane('ZX',origin=(0,-29,0))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-62,17),(-57,14)).arc((-53,-26),(-25,-58)).segment((-25,-72)).segment((25,-72)).segment((25,-69)).segment((30,-73)).segment((62,-17)).segment((57,-14)).arc((53,26),(25,58)).segment((25,72)).segment((-25,72)).segment((-25,69)).segment((-30,73)).close().assemble(),mode='s').finalize().extrude(-28).union(w1.sketch().push([(13,1)]).circle(87).circle(79,mode='s').finalize().extrude(59))