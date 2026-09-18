import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
r=w0.sketch().segment((-100,-62),(100,-62)).segment((100,-50)).segment((87,-50)).segment((87,62)).segment((-100,62)).close().assemble().push([(-81,-43)]).circle(12,mode='s').finalize().extrude(-25)