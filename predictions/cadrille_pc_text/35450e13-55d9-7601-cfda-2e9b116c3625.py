import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
r=w0.sketch().segment((-100,-62),(100,-62)).segment((100,62)).segment((98,62)).segment((98,60)).segment((94,60)).segment((94,62)).segment((-100,62)).close().assemble().push([(-69,32)]).circle(5,mode='s').push([(0,0)]).rect(148,26,mode='s').finalize().extrude(-24)