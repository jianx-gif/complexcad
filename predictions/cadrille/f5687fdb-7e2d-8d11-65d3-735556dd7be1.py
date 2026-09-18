import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,26,0))
w1=cq.Workplane('ZX',origin=(0,13,0))
r=w0.sketch().push([(10,0)]).circle(92).circle(74,mode='s').circle(50).finalize().extrude(-103).union(w0.sketch().push([(9,0)]).circle(37).circle(22,mode='s').finalize().extrude(51)).union(w1.sketch().segment((-100,-37),(-76,-37)).arc((100,5),(-80,10)).segment((-100,10)).close().assemble().reset().face(w1.sketch().arc((-74,-18),(-74,-20),(-73,-21)).segment((-73,-18)).close().assemble(),mode='s').push([(-10,0)]).circle(59,mode='s').finalize().extrude(-42))