import cadquery as cq
w0=cq.Workplane('ZX',origin=(-100,-62,-12))
r=w0.sketch().segment((-13,-100),(12,-100)).segment((13,100)).segment((-12,100)).close().assemble().push([(-5,19)]).circle(7,mode='s').finalize().extrude(124)