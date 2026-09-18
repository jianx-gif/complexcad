import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-26))
w1=cq.Workplane('XY',origin=(0,0,-33))
r=w0.sketch().segment((-100,-99),(69,-3)).segment((62,10)).segment((-100,99)).close().assemble().push([(-40,0)]).circle(26,mode='s').finalize().extrude(26).union(w1.workplane(offset=66/2).moveTo(86.5,0).box(27,40,66))