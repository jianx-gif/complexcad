import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,91))
w1=cq.Workplane('ZX',origin=(0,-83,0))
r=w0.sketch().segment((-63,45),(-61,-34)).segment((26,-32)).segment((24,47)).close().assemble().push([(12,1)]).circle(15,mode='s').finalize().extrude(-158).union(w1.sketch().segment((-100,-67),(-97,-67)).arc((-74,-23),(-38,10)).arc((-36,19),(-32,27)).arc((-29,43),(-23,58)).segment((-23,67)).segment((-100,67)).close().assemble().push([(-79,58)]).circle(3,mode='s').push([(-79,-14)]).circle(3,mode='s').push([(10,12)]).circle(12,mode='s').push([(10,58)]).circle(2,mode='s').finalize().extrude(179))