import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().segment((-100,-62),(100,-62)).segment((100,-15)).segment((93,-15)).segment((93,-48)).segment((90,-48)).segment((90,-15)).segment((-50,-12)).segment((-50,63)).segment((-100,62)).close().assemble().push([(24,-36)]).circle(8,mode='s').finalize().extrude(-20)