import cadquery as cq
w0=cq.Workplane('YZ',origin=(50,0,0))
r=w0.sketch().segment((-100,-19),(100,-19)).segment((100,19)).segment((25,19)).segment((25,1)).segment((-100,1)).segment((-100,-14)).arc((-97,-15),(-100,-16)).close().assemble().push([(-10,-15)]).circle(1,mode='s').push([(63,-7)]).circle(5,mode='s').push([(98,10)]).circle(2,mode='s').finalize().extrude(-100)