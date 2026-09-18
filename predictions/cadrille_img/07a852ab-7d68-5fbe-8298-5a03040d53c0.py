import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-26,0))
w1=cq.Workplane('ZX',origin=(0,-60,0))
r=w0.sketch().segment((-35,-79),(-35,-70)).arc((0,-77),(35,-70)).segment((35,-79)).arc((77,-47),(97,4)).segment((35,4)).segment((35,13)).segment((97,13)).arc((77,64),(35,96)).segment((35,87)).arc((0,94),(-35,87)).segment((-35,96)).arc((-77,44),(-73,-23)).arc((-74,-26),(-74,-29)).arc((-76,-54),(-60,-73)).arc((-41,-78),(-22,-79)).close().assemble().finalize().extrude(102).union(w1.sketch().push([(12,11)]).circle(88).circle(87,mode='s').finalize().extrude(109))