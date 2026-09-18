import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,21,0))
w1=cq.Workplane('ZX',origin=(0,39,0))
r=w0.sketch().segment((-1,-85),(1,-85)).segment((1,-84)).arc((84,0),(1,84)).segment((1,85)).segment((-1,85)).segment((-1,84)).arc((-84,0),(-1,-84)).close().assemble().push([(16,31)]).circle(58,mode='s').finalize().extrude(-11).union(w1.sketch().push([(13,16)]).circle(87).circle(58,mode='s').finalize().extrude(-78))