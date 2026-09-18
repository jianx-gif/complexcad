import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,34,0))
w1=cq.Workplane('ZX',origin=(0,88,0))
r=w0.sketch().segment((-100,-4),(-83,-4)).arc((0,-83),(83,-4)).segment((100,-4)).segment((100,4)).segment((83,4)).arc((0,83),(-83,4)).segment((-100,4)).close().assemble().circle(55,mode='s').finalize().extrude(-67).union(w1.sketch().push([(6,11)]).circle(89).circle(39,mode='s').finalize().extrude(-156))