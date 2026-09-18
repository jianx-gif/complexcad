import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-10))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().push([(0,-1)]).circle(29).push([(-22,-10)]).circle(2,mode='s').finalize().extrude(26).union(w1.sketch().segment((-16,-72),(-10,-72)).segment((-10,-80)).segment((6,-80)).segment((6,80)).segment((-10,80)).segment((-10,-64)).segment((-16,-64)).close().assemble().push([(3,36)]).circle(2,mode='s').finalize().extrude(200))