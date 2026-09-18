import cadquery as cq
w0=cq.Workplane('YZ',origin=(-50,0,0))
r=w0.sketch().segment((-100,-19),(100,-19)).segment((100,19)).segment((25,19)).segment((25,1)).segment((-100,1)).close().assemble().push([(-15,-16)]).circle(2,mode='s').push([(64,-10)]).circle(5,mode='s').finalize().extrude(100)