import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,-100,-3))
r=w0.sketch().segment((-53,16),(-53,18)).segment((-51,18)).segment((-51,15)).arc((-49,19),(-53,16)).assemble().finalize().extrude(-31).union(w0.sketch().push([(50,-10)]).circle(25).push([(50,-9.5)]).rect(24,23,mode='s').finalize().extrude(37)).union(w0.workplane(offset=103/2).moveTo(50,-10).cylinder(103,2))