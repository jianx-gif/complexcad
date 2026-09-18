import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,98,0))
w1=cq.Workplane('ZX',origin=(0,50,0))
r=w0.sketch().arc((-60,-66),(-4,-91),(53,-66)).segment((48,-66)).arc((-4,-90),(-56,-66)).close().assemble().reset().face(w0.sketch().segment((-60,66),(-56,66)).arc((-4,90),(48,66)).segment((53,66)).arc((-4,91),(-60,66)).assemble()).finalize().extrude(-144).union(w1.sketch().push([(-4,38)]).circle(36).circle(33,mode='s').finalize().extrude(-100))