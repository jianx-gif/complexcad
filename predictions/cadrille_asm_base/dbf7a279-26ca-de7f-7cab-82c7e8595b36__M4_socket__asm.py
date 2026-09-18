import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-6))
w1=cq.Workplane('ZX',origin=(0,75,0))
r=w0.sketch().segment((-100,-75),(100,-75)).segment((100,75)).segment((-100,75)).segment((-100,-29)).segment((-77,-29)).segment((-77,-56)).segment((-100,-56)).close().assemble().push([(80,-28)]).circle(25,mode='s').finalize().extrude(10).union(w0.workplane(offset=25/2).cylinder(25,25)).union(w1.sketch().arc((-19,75),(0,40),(19,75)).segment((13,75)).arc((0,70),(-13,75)).close().assemble().finalize().extrude(-133))