import cadquery as cq
w0=cq.Workplane('YZ',origin=(45,0,0))
w1=cq.Workplane('ZX',origin=(0,-82,0))
r=w0.sketch().segment((-35,89),(-33,-91)).segment((35,-90)).segment((33,91)).close().assemble().push([(65,-67)]).circle(32).finalize().extrude(-102).union(w1.sketch().push([(0,10.5)]).rect(200,101).push([(0,10)]).circle(89,mode='s').push([(84,48)]).circle(9,mode='s').finalize().extrude(179))