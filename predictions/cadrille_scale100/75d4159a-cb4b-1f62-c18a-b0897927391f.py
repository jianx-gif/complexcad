import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,20))
w1=cq.Workplane('ZX',origin=(0,-18,0))
r=w0.sketch().segment((-40,-12),(40,-12)).segment((40,0)).segment((-34,0)).arc((-37,-6),(-40,-12)).assemble().push([(20,-7)]).circle(6,mode='s').finalize().extrude(-40).union(w1.workplane(offset=23/2).moveTo(0,2).cylinder(23,8))