import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,90,0))
w1=cq.Workplane('ZX',origin=(0,10,0))
r=w0.sketch().segment((-92,-46),(-91,-46)).arc((-89,-34),(-86,-23)).arc((-88,-19),(-90,-15)).close().assemble().reset().face(w0.sketch().arc((-86,-13),(-84,-10),(-81,-8)).arc((-7,86),(92,23)).segment((92,46)).segment((91,46)).arc((0,92),(-91,46)).segment((-92,46)).close().assemble()).finalize().extrude(-79).union(w1.sketch().arc((-69,-27),(-55,-33),(-43,-44)).arc((57,28),(-69,-27)).assemble().circle(53,mode='s').finalize().extrude(-70))