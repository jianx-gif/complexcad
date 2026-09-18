import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-77,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-1,-78),(43,-43),(78,2)).segment((78,3)).arc((60,43),(42,83)).segment((42,84)).segment((-1,84)).close().assemble().finalize().extrude(165).union(w1.sketch().circle(100).push([(-1,-1)]).circle(46,mode='s').finalize().extrude(74))