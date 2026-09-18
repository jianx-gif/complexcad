import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,59,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().segment((-97,-3),(-57,-3)).arc((-59,0),(-57,3)).segment((-97,3)).close().assemble().reset().face(w0.sketch().segment((57,-3),(97,-3)).segment((97,3)).segment((57,3)).arc((59,0),(57,-3)).assemble()).finalize().extrude(-117).union(w1.sketch().segment((-100,-19),(-98,-19)).arc((0,-100),(98,-19)).segment((100,-19)).segment((100,19)).segment((98,19)).arc((0,100),(-98,19)).segment((-100,19)).close().assemble().circle(99,mode='s').finalize().extrude(-175))