import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,62,0))
r=w0.sketch().segment((-13,-100),(12,-100)).segment((13,100)).segment((-12,100)).close().assemble().push([(-5,19)]).circle(6,mode='s').finalize().extrude(-125)