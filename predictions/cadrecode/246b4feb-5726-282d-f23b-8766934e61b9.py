import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-75,0))
r=w0.sketch().segment((-6,-99),(-5,-99)).segment((-5,-100)).segment((5,-100)).segment((5,-99)).segment((6,-99)).segment((6,99)).segment((5,99)).segment((5,100)).segment((-5,100)).segment((-5,99)).segment((-6,99)).close().assemble().push([(-1,84)]).circle(9,mode='s').push([(0,0)]).circle(12,mode='s').finalize().extrude(149)