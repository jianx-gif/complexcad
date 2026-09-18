import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-96,0))
w1=cq.Workplane('ZX',origin=(0,-61,0))
r=w0.workplane(offset=192/2).cylinder(192,19).union(w1.sketch().segment((-100,-17),(-97,-17)).arc((0,-98),(97,-17)).segment((100,-17)).segment((100,17)).segment((97,17)).arc((0,98),(-97,17)).segment((-100,17)).close().assemble().circle(89,mode='s').finalize().extrude(-39))