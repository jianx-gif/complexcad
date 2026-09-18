import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-64))
r=w0.sketch().segment((91,-18),(100,-18)).segment((100,18)).segment((92,18)).arc((-100,1),(91,-18)).assemble().push([(-4,0)]).circle(83,mode='s').finalize().extrude(128)