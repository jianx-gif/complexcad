import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,20))
w1=cq.Workplane('ZX',origin=(0,5,0))
r=w0.sketch().push([(0,-6)]).rect(80,12).push([(-24,-5)]).circle(2,mode='s').push([(19,-6)]).circle(6,mode='s').finalize().extrude(-40).union(w0.sketch().segment((-11,-12),(11,-12)).segment((11,-1)).segment((-11,-1)).segment((-11,-3)).arc((-10,-4),(-11,-5)).close().assemble().finalize().extrude(-39)).union(w1.workplane(offset=-23/2).moveTo(0,2).cylinder(23,7))
