import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-18))
r=w0.sketch().segment((-100,-22),(78,-22)).segment((78,-11)).segment((100,-11)).segment((100,11)).segment((78,11)).segment((78,22)).segment((-100,22)).close().assemble().push([(-56,0)]).circle(7,mode='s').finalize().extrude(23).union(w0.sketch().push([(-11,0)]).rect(152,26).push([(-49.5,0)]).rect(37,12,mode='s').finalize().extrude(36))