import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-39,0))
w1=cq.Workplane('ZX',origin=(0,-19,0))
r=w0.workplane(offset=-10/2).cylinder(10,93).union(w0.sketch().segment((-49,-29),(49,-29)).segment((49,29)).segment((-49,29)).segment((-49,21)).arc((-52,13),(-49,5)).close().assemble().finalize().extrude(124)).union(w1.sketch().segment((-100,-19),(-96,-19)).arc((0,-100),(96,-19)).segment((100,-19)).segment((100,19)).segment((96,19)).arc((0,100),(-96,19)).segment((-100,19)).close().assemble().circle(99,mode='s').finalize().extrude(79))