import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-11,0))
w1=cq.Workplane('XY',origin=(0,0,-8))
r=w0.sketch().segment((-14,100),(-5,48)).arc((-3,49),(1,49)).segment((-8,100)).close().assemble().reset().face(w0.sketch().segment((-4,-49),(3,-49)).segment((3,-48)).arc((-1,-48),(-4,-49)).assemble()).reset().face(w0.sketch().segment((-3,48),(2,-47)).arc((2,1),(-3,48)).assemble()).finalize().extrude(22).union(w1.sketch().push([(-84,0)]).circle(13).push([(-84.5,0)]).rect(7,2,mode='s').finalize().extrude(21))