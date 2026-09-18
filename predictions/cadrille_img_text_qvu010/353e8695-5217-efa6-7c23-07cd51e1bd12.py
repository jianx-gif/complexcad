import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-77,0))
r=w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(143).union(w0.sketch().arc((-100,-19),(0,-100),(100,-19)).segment((98,-19)).arc((0,-99),(-98,-19)).close().assemble().reset().face(w0.sketch().segment((-100,19),(-98,19)).arc((0,99),(98,19)).segment((100,19)).arc((0,100),(-100,19)).assemble()).finalize().extrude(177))