import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('XY',origin=(0,0,16))
r=w0.sketch().segment((-20,-38),(20,-38)).segment((20,-19)).arc((0,-31),(-20,-19)).close().assemble().finalize().extrude(16).union(w0.sketch().segment((-40,-30),(36,-30)).segment((36,30)).segment((-39,30)).arc((-39,28),(-40,27)).close().assemble().finalize().extrude(20)).union(w1.sketch().push([(0,-4)]).rect(80,50).push([(0,-3.5)]).rect(20,63,mode='s').finalize().extrude(-16))
