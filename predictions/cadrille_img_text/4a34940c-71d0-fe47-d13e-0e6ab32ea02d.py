import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,98,0))
w1=cq.Workplane('ZX',origin=(0,83,0))
r=w0.sketch().arc((-42,-90),(0,-100),(42,-90)).segment((39,-90)).arc((0,-99),(-39,-90)).close().assemble().reset().face(w0.sketch().segment((-42,90),(-39,90)).arc((0,99),(39,90)).segment((42,90)).arc((0,100),(-42,90)).assemble()).finalize().extrude(-176).union(w1.sketch().push([(8,10)]).circle(90).circle(87,mode='s').finalize().extrude(-167))