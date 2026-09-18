import cadquery as cq
w0=cq.Workplane('YZ',origin=(0,0,0))
w1=cq.Workplane('XY',origin=(0,0,40))
r=w0.sketch().segment((-33,-27),(14,-40)).segment((33,27)).segment((-14,40)).close().assemble().finalize().extrude(-20).union(w1.sketch().segment((-100,-67),(100,-67)).segment((100,67)).segment((-100,67)).segment((-100,0)).segment((0,0)).segment((0,-66)).segment((-100,-66)).close().assemble().push([(-25,25)]).circle(2,mode='s').push([(25,-25)]).circle(2,mode='s').finalize().extrude(-67))