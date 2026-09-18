import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-18,0))
w1=cq.Workplane('XY',origin=(0,0,-95))
r=w0.sketch().push([(-75,0)]).circle(15).circle(13,mode='s').finalize().extrude(-12).union(w0.sketch().push([(75,-55)]).circle(15).circle(10,mode='s').finalize().extrude(25)).union(w1.sketch().segment((-97,-19),(-79,-19)).arc((0,-73),(79,-19)).segment((97,-19)).segment((97,19)).segment((79,19)).arc((0,73),(-79,19)).segment((-97,19)).close().assemble().finalize().extrude(195))