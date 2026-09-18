import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-9))
r=w0.sketch().segment((-100,-75),(100,-75)).segment((100,75)).segment((-97,75)).arc((-98,73),(-100,72)).close().assemble().push([(-29,-56.5)]).rect(130,11,mode='s').finalize().extrude(10).union(w0.workplane(offset=18/2).box(50,100,18))