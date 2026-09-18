import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,3))
w1=cq.Workplane('ZX',origin=(0,-4,0))
r=w0.sketch().segment((-100,-49),(99,-50)).segment((100,50)).segment((-99,50)).close().assemble().push([(74,1)]).circle(28,mode='s').finalize().extrude(-6).union(w0.sketch().circle(79).push([(63,-24)]).circle(10,mode='s').finalize().extrude(6)).union(w1.workplane(offset=69/2).moveTo(0,-75).cylinder(69,9))