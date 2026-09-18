import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().circle(100).circle(93,mode='s').finalize().extrude(-200).union(w0.sketch().arc((-100,-19),(0,-100),(100,-19)).segment((58,-19)).arc((0,-70),(-58,-19)).close().assemble().finalize().extrude(-175))