import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-60))
w1=cq.Workplane('XY',origin=(0,0,-31))
r=w0.sketch().segment((-70,-72),(-60,-72)).arc((0,-99),(60,-72)).segment((70,-72)).segment((70,-65)).arc((99,-11),(79,46)).arc((75,59),(68,72)).segment((60,72)).arc((0,99),(-60,72)).segment((-70,72)).segment((-70,65)).arc((-99,0),(-70,-65)).close().assemble().push([(0,2)]).circle(54,mode='s').finalize().extrude(120).union(w1.sketch().arc((-99,-13),(99,-11),(-97,22)).arc((-100,5),(-99,-13)).assemble().finalize().extrude(57))