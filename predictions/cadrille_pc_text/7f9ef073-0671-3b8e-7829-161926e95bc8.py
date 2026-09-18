import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,31))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().push([(-2,0)]).circle(93).circle(47,mode='s').finalize().extrude(-62).union(w1.sketch().arc((12,-3),(26,18),(12,39)).close().assemble().finalize().extrude(-200))