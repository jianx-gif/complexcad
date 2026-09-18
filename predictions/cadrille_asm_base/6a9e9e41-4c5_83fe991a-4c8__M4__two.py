import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-19))
w1=cq.Workplane('YZ',origin=(-56,0,0))
r=w0.sketch().push([(-18.5,-53.5)]).rect(149,93).push([(-18,-53)]).circle(12,mode='s').finalize().extrude(-9).union(w1.sketch().segment((-85,-19),(100,-19)).segment((100,37)).segment((-71,37)).segment((-71,35)).segment((-73,35)).segment((-73,37)).segment((-85,37)).close().assemble().push([(7,9)]).rect(168,38,mode='s').finalize().extrude(149))