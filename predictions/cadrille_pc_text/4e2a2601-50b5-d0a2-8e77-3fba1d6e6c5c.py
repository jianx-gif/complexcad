import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().segment((-100,-62),(100,-62)).segment((100,-14)).segment((93,-14)).segment((93,-12)).segment((-50,-12)).segment((-50,63)).segment((-100,62)).segment((-100,-48)).arc((-97,-50),(-100,-52)).close().assemble().push([(24,-36)]).circle(8,mode='s').finalize().extrude(-20)