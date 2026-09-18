import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,13))
w1=cq.Workplane('ZX',origin=(0,50,0))
r=w0.sketch().segment((-33,-16),(33,-16)).segment((33,16)).segment((-33,16)).segment((-33,10)).arc((-30,8),(-33,6)).close().assemble().rect(16,16,mode='s').finalize().extrude(-11).union(w1.sketch().push([(-3.5,0)]).rect(19,200).rect(7,16,mode='s').push([(-3,-67)]).circle(3,mode='s').finalize().extrude(-100))