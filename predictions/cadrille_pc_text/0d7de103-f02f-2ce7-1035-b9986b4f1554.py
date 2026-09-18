import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-20))
w1=cq.Workplane('ZX',origin=(0,10,0))
r=w0.sketch().segment((-100,-42),(-82,-42)).segment((-82,-50)).segment((88,-50)).segment((88,-42)).segment((100,-42)).segment((100,42)).segment((88,42)).segment((88,50)).segment((-82,50)).segment((-82,42)).segment((-100,42)).close().assemble().push([(-88.5,-16.5)]).rect(13,33,mode='s').finalize().extrude(40).union(w1.sketch().push([(0,27)]).circle(33).push([(0,27.5)]).rect(34,39,mode='s').finalize().extrude(-52))