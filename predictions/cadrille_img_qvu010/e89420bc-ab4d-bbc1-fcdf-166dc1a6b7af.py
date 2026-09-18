import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,6,0))
w1=cq.Workplane('ZX',origin=(0,73,0))
r=w0.sketch().segment((-100,-34),(-68,83)).arc((-89,58),(-100,29)).close().assemble().reset().face(w0.sketch().arc((-100,-29),(-89,-58),(-68,-83)).close().assemble()).reset().face(w0.sketch().segment((-19,83),(100,34)).segment((100,39)).arc((46,68),(-19,83)).assemble()).reset().face(w0.sketch().arc((68,-83),(89,-58),(100,-29)).close().assemble()).finalize().extrude(-6).union(w1.sketch().circle(83).push([(-72,-18)]).circle(14,mode='s').push([(72,10)]).circle(13,mode='s').finalize().extrude(-146))